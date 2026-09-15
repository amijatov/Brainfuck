from instructionset import ADD, MOVE, SET, LOOP


KEEP = object()


def _merge(left, right):
    """Prüft, ob zwei benachbarte Befehle zusammengefasst werden können."""
    left_operation = left[0]
    right_operation = right[0]

    if left_operation == ADD and right_operation == ADD:
        value = (left[1] + right[1]) % 256
        return None if value == 0 else (ADD, value)

    if left_operation == MOVE and right_operation == MOVE:
        if left[1] * right[1] <= 0:
            return KEEP
        return (MOVE, left[1] + right[1])

    if left_operation == SET and right_operation == ADD:
        return (SET, (left[1] + right[1]) % 256)

    if left_operation == SET and right_operation == SET:
        return right

    if left_operation == ADD and right_operation == SET:
        return right

    return KEEP


def peephole(instructions):
    """Vereinfacht benachbarte Befehle durch lokale Ersetzungsregeln."""
    output = []
    for instruction in instructions:
        if instruction[0] == LOOP:
            instruction = (LOOP, peephole(instruction[1]))

        output.append(instruction)
        while len(output) >= 2:
            merged = _merge(output[-2], output[-1])
            if merged is KEEP:
                break
            if merged is None:
                del output[-2:]
            else:
                output[-2:] = [merged]
    return output
