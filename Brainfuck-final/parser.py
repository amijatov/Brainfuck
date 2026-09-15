from instructionset import ADD, MOVE, OUTPUT, INPUT, LOOP


def parse(code, coalesce=True):
    """Übersetzt Brainfuck in eine Baumdarstellung der Befehle."""
    root = []
    stack = [root]
    index = 0

    while index < len(code):
        command = code[index]

        if command in "+-":
            if not coalesce:
                stack[-1].append((ADD, 1 if command == "+" else -1))
                index += 1
                continue

            amount = 0
            while index < len(code) and code[index] in "+-":
                amount += 1 if code[index] == "+" else -1
                index += 1
            if amount % 256 != 0:
                stack[-1].append((ADD, amount))
            continue

        if command in "><":
            if not coalesce:
                stack[-1].append((MOVE, 1 if command == ">" else -1))
                index += 1
                continue

            direction = 1 if command == ">" else -1
            amount = 0
            while index < len(code) and code[index] == command:
                amount += direction
                index += 1
            stack[-1].append((MOVE, amount))
            continue

        if command == ".":
            stack[-1].append((OUTPUT,))
        elif command == ",":
            stack[-1].append((INPUT,))
        elif command == "[":
            body = []
            stack[-1].append((LOOP, body))
            stack.append(body)
        elif command == "]":
            if len(stack) == 1:
                raise SyntaxError("Unmatched ']'")
            stack.pop()

        index += 1

    if len(stack) != 1:
        raise SyntaxError("Unmatched '['")
    return root
