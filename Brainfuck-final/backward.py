from instructionset import ADD, MOVE, SET, MULADD, OUTPUT, INPUT, LOOP
from loop_analysis import net_move


BACKWARDS_FIXPOINT_LIMIT = 16


def backwards(instructions):
    """Entfernt nicht benötigte Zelländerungen durch Rückwärtsanalyse."""
    try:
        cleaned, _live, _all_live = _backwards_sequence(instructions, set(), False)
        return cleaned
    except RecursionError:
        return instructions


def _backwards_sequence(sequence, live, all_live):
    """Bestimmt benötigte Zellwerte und bereinigt eine Befehlsfolge."""
    live = set(live)
    reversed_output = []

    for instruction in reversed(sequence):
        operation = instruction[0]

        if operation == OUTPUT:
            live.add(0)
            reversed_output.append(instruction)

        elif operation == INPUT:
            reversed_output.append(instruction)

        elif operation == SET:
            if all_live or 0 in live:
                live.discard(0)
                reversed_output.append(instruction)

        elif operation == ADD:
            if all_live or 0 in live:
                live.add(0)
                reversed_output.append(instruction)

        elif operation == MOVE:
            amount = instruction[1]
            live = {offset + amount for offset in live}
            reversed_output.append(instruction)

        elif operation == MULADD:
            live.add(0)
            for offset, _factor in instruction[1]:
                live.add(offset)
            reversed_output.append(instruction)

        elif operation == LOOP:
            live, all_live = _backwards_loop(
                instruction[1], live, all_live, reversed_output
            )

        else:
            live, all_live = set(), True
            reversed_output.append(instruction)

    reversed_output.reverse()
    return reversed_output, live, all_live


def _backwards_loop(body, live_after, all_live_after, reversed_output):
    """Bestimmt benötigte Zellwerte einer Schleife und bereinigt ihren Rumpf."""
    if net_move(body) != 0:
        cleaned, _, _ = _backwards_sequence(body, set(), True)
        reversed_output.append((LOOP, cleaned))
        return set(), True

    after = set(live_after)
    current_live = after | {0}
    current_all = all_live_after

    for _ in range(BACKWARDS_FIXPOINT_LIMIT):
        _, body_live, body_all = _backwards_sequence(
            body, current_live, current_all
        )
        new_live = after | {0} | body_live
        new_all = all_live_after or body_all
        if new_live == current_live and new_all == current_all:
            break
        current_live, current_all = new_live, new_all
    else:
        current_live, current_all = set(), True

    cleaned, _, _ = _backwards_sequence(body, current_live, current_all)
    reversed_output.append((LOOP, cleaned))
    return current_live, current_all
