from instructionset import ADD, SET, LOOP


def is_clear_loop(body):
    """Prüft, ob ein Schleifenrumpf die aktuelle Zelle sicher löscht."""
    if len(body) != 1:
        return False

    instruction = body[0]
    operation = instruction[0]

    if operation == ADD and instruction[1] % 2 == 1:
        return True

    return operation == SET and instruction[1] % 256 == 0


def rewrite_clear_loops(instructions):
    """Ersetzt erkannte Löschschleifen durch SET 0."""
    output = []
    for instruction in instructions:
        if instruction[0] != LOOP:
            output.append(instruction)
            continue

        body = rewrite_clear_loops(instruction[1])
        if is_clear_loop(body):
            output.append((SET, 0))
        else:
            output.append((LOOP, body))
    return output
