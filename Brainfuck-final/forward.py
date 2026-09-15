from analysis_domain import (
    CELL_TOP,
    ZERO,
    State,
    const_interval,
    wrap_add,
    wrap_add_intervals,
    wrap_multiply,
)
from instructionset import ADD, MOVE, SET, MULADD, SCAN, OUTPUT, INPUT, LOOP
from loop_analysis import linear_effect


FORWARD_FIXPOINT_LIMIT = 8


def forward(instructions):
    """Vereinfacht Befehle mithilfe der Vorwärtsanalyse."""
    output = []
    _forward_sequence(instructions, State.initial(), output)
    return output


def _forward_sequence(sequence, state, output):
    """Analysiert eine Befehlsfolge und sammelt bei Bedarf vereinfachte Befehle."""
    for instruction in sequence:
        operation = instruction[0]

        if operation == LOOP:
            state = _forward_loop(instruction[1], state, output)
            continue

        if operation == ADD:
            amount = instruction[1]
            if amount % 256 == 0:
                continue

            old_value = state.read()
            if old_value.is_const():
                new_value = const_interval(old_value.lo + amount)
                state.write(new_value)
                if output is not None:
                    output.append((SET, new_value.lo))
                continue
            state.write(wrap_add(old_value, amount))

        elif operation == SET:
            new_value = const_interval(instruction[1])
            old_value = state.read()
            if old_value.is_const() and old_value == new_value:
                continue
            state.write(new_value)

        elif operation == MOVE:
            state.move(instruction[1])

        elif operation == MULADD:
            guard = state.read()
            if guard.is_zero():
                continue
            for offset, factor in instruction[1]:
                old_target = state.read_at(offset)
                addition = wrap_multiply(guard, factor)
                state.write_at(offset, wrap_add_intervals(old_target, addition))
            state.write(ZERO)

        elif operation == SCAN:
            if instruction[1] > 0:
                state.forget_pointer(state.ptr.lo, None)
            else:
                state.forget_pointer(None, state.ptr.hi)
            state.cur = ZERO

        elif operation == INPUT:
            state.write(CELL_TOP)

        elif operation == OUTPUT:
            pass


        if output is not None:
            output.append(instruction)

    return state


def _forward_loop(body, state, output):
    """Analysiert eine Schleife und vereinfacht sie bei Bedarf."""
    guard = state.read()
    if guard.is_zero():
        return state

    entry = state.copy()
    entry.write(guard.without_zero())

    counted = _solve_balanced_counted_loop(body, entry) if guard.is_const() else None

    runs_once = counted is not None and counted[0] == 1
    if runs_once:
        head = entry
    else:
        head = _find_loop_invariant(body, entry)


    if output is not None:
        transformed_body = []
        _forward_sequence(body, head.copy(), transformed_body)
        if runs_once:
            output.extend(transformed_body)
        else:
            output.append((LOOP, transformed_body))

    if counted is not None:
        return counted[1]

    post = _forward_sequence(body, head.copy(), None)
    post = state.join(post)
    post.write(ZERO)
    return post


def _find_loop_invariant(body, entry):
    """Sucht eine stabile Zustandsbeschreibung für den Schleifenkopf."""
    head = entry
    for _ in range(FORWARD_FIXPOINT_LIMIT):
        candidate = _loop_step(body, entry, head)
        if candidate.leq(head):
            return head

        head = head.widen(head.join(candidate))

    return State.unknown()


def _loop_step(body, entry, head):
    """Berechnet mögliche Zustände für den nächsten Schleifendurchlauf."""
    after_body = _forward_sequence(body, head.copy(), None)
    joined = entry.join(after_body)

    guard = joined.read()
    if not guard.is_zero():
        joined.write(guard.without_zero())
    return joined


def _solve_balanced_counted_loop(body, entry):
    """Berechnet Durchlaufzahl und Nachzustand einer geeigneten Schleife."""

    effect = linear_effect(body)
    if effect is None:
        return None

    net_pointer_move, deltas = effect
    if net_pointer_move != 0:
        return None


    guard = entry.read()
    guard_delta = deltas.get(0, 0) % 256
    if guard_delta % 2 == 0:
        return None

    iterations = (-guard.lo * pow(guard_delta, -1, 256)) % 256

    post = entry.copy()
    for offset, delta in deltas.items():
        old_value = post.read_at(offset)
        post.write_at(offset, wrap_add(old_value, delta * iterations))
    post.write(ZERO)
    return iterations, post
