from instructionset import ADD, MOVE, SCAN, LOOP


def linear_effect_with_accesses(body):
    """Ermittelt Zeigerbewegung, Zelländerungen und besuchte Bewegungsoffsets."""
    offset = 0
    deltas = {}
    accesses = []
    seen_accesses = set()
    for instruction in body:
        operation = instruction[0]
        if operation == ADD:
            deltas[offset] = deltas.get(offset, 0) + instruction[1]
        elif operation == MOVE:
            offset += instruction[1]
            if offset != 0 and offset not in seen_accesses:
                seen_accesses.add(offset)
                accesses.append(offset)
        else:
            return None
    return offset, deltas, accesses


def linear_effect(body):
    """Ermittelt die Nettozeigerbewegung und die Zelländerungen eines Rumpfs."""
    result = linear_effect_with_accesses(body)
    if result is None:
        return None
    offset, deltas, _accesses = result
    return offset, deltas


def net_move(sequence):
    """Bestimmt die Nettozeigerbewegung, sofern sie statisch bekannt ist."""
    total = 0
    for instruction in sequence:
        operation = instruction[0]
        if operation == MOVE:
            total += instruction[1]
        elif operation == SCAN:
            return None
        elif operation == LOOP and net_move(instruction[1]) != 0:
            return None
    return total
