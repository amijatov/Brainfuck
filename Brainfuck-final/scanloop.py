from instructionset import MOVE, SCAN, LOOP


def rewrite_scan_loops(instructions):
    """Ersetzt erkannte Suchschleifen durch SCAN."""
    output = []
    for instruction in instructions:
        if instruction[0] != LOOP:
            output.append(instruction)
            continue

        body = rewrite_scan_loops(instruction[1])
        if len(body) == 1 and body[0][0] == MOVE and body[0][1] != 0:
            output.append((SCAN, body[0][1]))
        else:
            output.append((LOOP, body))
    return output
