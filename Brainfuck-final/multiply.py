from instructionset import SET, MULADD, LOOP
from loop_analysis import linear_effect_with_accesses


def rewrite_multiply_loops(instructions):
    """Ersetzt geeignete Schleifen durch MULADD oder SET 0."""
    output = []
    for instruction in instructions:
        if instruction[0] != LOOP:
            output.append(instruction)
            continue

        body = rewrite_multiply_loops(instruction[1])
        targets = multiply_targets(body)
        if targets is None:
            output.append((LOOP, body))
        elif targets:
            output.append((MULADD, tuple(targets)))
        else:
            output.append((SET, 0))
    return output


def multiply_targets(body):
    """Bestimmt Zieloffsets und Faktoren einer geeigneten Multiplikationsschleife."""
    effect = linear_effect_with_accesses(body)
    if effect is None:
        return None

    net_pointer_move, deltas, accesses = effect
    if net_pointer_move != 0:
        return None

    if deltas.get(0, 0) % 256 != 255:
        return None

    return [(offset, deltas.get(offset, 0) % 256) for offset in accesses]
