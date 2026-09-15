from instructionset import LOOP, JZ, JNZ
from optimizer import optimize_bf
from parser import parse


def process(code, optimize=True, coalesce=True, passes=None):
    """Parst den Quelltext und optimiert die Baumdarstellung bei Bedarf."""
    instructions = parse(code, coalesce=coalesce)
    if optimize:
        instructions = optimize_bf(instructions, passes=passes)
    return instructions


def to_bytecode(code, optimize=True, coalesce=True, passes=None):
    """Übersetzt Brainfuck in flachen Bytecode."""
    return flatten(process(code, optimize, coalesce, passes))


def flatten(instructions):
    """Ersetzt Schleifenknoten durch eine flache Befehlsfolge mit Sprüngen."""
    bytecode = []
    stack = [(iter(instructions), None)]
    while stack:
        iterator, jump_if_zero_position = stack[-1]
        try:
            instruction = next(iterator)
        except StopIteration:
            stack.pop()
            if jump_if_zero_position is not None:
                bytecode.append((JNZ, jump_if_zero_position + 1))
                bytecode[jump_if_zero_position] = (JZ, len(bytecode))
            continue

        if instruction[0] != LOOP:
            bytecode.append(instruction)
            continue

        nested_jump_position = len(bytecode)
        bytecode.append((JZ, None))
        stack.append((iter(instruction[1]), nested_jump_position))
    return bytecode
