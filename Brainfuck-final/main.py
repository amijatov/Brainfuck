import argparse

from instructionset import LOOP
from interpreter import run
from pipeline import flatten, process


def show_ir(instructions, depth=0):
    """Gibt die Baumdarstellung der Befehle eingerückt aus."""
    stack = [(iter(instructions), depth, None)]
    while stack:
        iterator, current_depth, closing_depth = stack[-1]
        try:
            instruction = next(iterator)
        except StopIteration:
            stack.pop()
            if closing_depth is not None:
                print(f"{'  ' * closing_depth}END")
            continue

        indentation = "  " * current_depth
        if instruction[0] == LOOP:
            print(f"{indentation}LOOP")
            stack.append((iter(instruction[1]), current_depth + 1, current_depth))
        elif len(instruction) == 1:
            print(f"{indentation}{instruction[0]}")
        else:
            print(f"{indentation}{instruction[0]} {instruction[1]}")


def show_bytecode(bytecode):
    """Gibt flachen Bytecode mit Befehlsindizes aus."""
    for index, instruction in enumerate(bytecode):
        argument = "" if len(instruction) == 1 else f" {instruction[1]}"
        print(f"{index:5d}  {instruction[0]}{argument}")


def main():
    """Liest die Kommandozeilenoptionen und startet Anzeige oder Ausführung."""
    parser = argparse.ArgumentParser(
        description="Optimierender Brainfuck-Interpreter"
    )
    parser.add_argument("file", help="Pfad zu einer Brainfuck-Datei")
    parser.add_argument("--no-opt", action="store_true", help="Optimierungen aus")
    parser.add_argument("--no-coalesce", action="store_true", help="Parser-RLE aus")
    parser.add_argument("--show-ir", action="store_true", help="Baum-IR anzeigen")
    parser.add_argument(
        "--show-bytecode", action="store_true", help="flachen Bytecode anzeigen"
    )
    parser.add_argument("--tape-size", type=int, default=30_000)
    arguments = parser.parse_args()

    with open(arguments.file, encoding="utf-8") as source_file:
        code = source_file.read()

    instructions = process(
        code,
        optimize=not arguments.no_opt,
        coalesce=not arguments.no_coalesce,
    )

    if arguments.show_ir:
        show_ir(instructions)
        return

    bytecode = flatten(instructions)
    if arguments.show_bytecode:
        show_bytecode(bytecode)
        return

    run(bytecode, tape_size=arguments.tape_size)


if __name__ == "__main__":
    main()
