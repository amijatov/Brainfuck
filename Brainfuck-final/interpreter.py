import sys

from instructionset import ADD, MOVE, SET, MULADD, SCAN, OUTPUT, INPUT, JZ, JNZ


def run(bytecode, tape_size=30_000, inp=None, out=None, max_jumps=None):
    """Führt flachen Bytecode auf einem endlichen Byteband aus."""
    if tape_size <= 0:
        raise ValueError("tape_size muss positiv sein")

    if inp is None:
        inp = getattr(sys.stdin, "buffer", sys.stdin)
    if out is None:
        stdout = getattr(sys.stdout, "buffer", sys.stdout)
        out = getattr(stdout, "raw", stdout)

    tape = bytearray(tape_size)
    pointer = 0
    program_counter = 0
    jump_count = 0

    while program_counter < len(bytecode):
        instruction = bytecode[program_counter]
        operation = instruction[0]

        if operation == ADD:
            tape[pointer] = (tape[pointer] + instruction[1]) & 255

        elif operation == MOVE:
            pointer += instruction[1]
            if pointer < 0:
                raise RuntimeError("Pointer moved below 0")
            if pointer >= tape_size:
                raise RuntimeError("Pointer moved past end of tape")

        elif operation == JNZ:
            if tape[pointer]:
                jump_count += 1
                if max_jumps is not None and jump_count > max_jumps:
                    raise RuntimeError("jump limit exceeded")
                program_counter = instruction[1]
                continue

        elif operation == JZ:
            if not tape[pointer]:
                program_counter = instruction[1]
                continue

        elif operation == SET:
            tape[pointer] = instruction[1] & 255

        elif operation == MULADD:
            guard = tape[pointer]
            if guard:
                for offset, factor in instruction[1]:
                    target = pointer + offset
                    if target < 0:
                        raise RuntimeError("Pointer moved below 0")
                    if target >= tape_size:
                        raise RuntimeError("Pointer moved past end of tape")
                    tape[target] = (tape[target] + factor * guard) & 255
            tape[pointer] = 0

        elif operation == SCAN:
            step = instruction[1]
            if step == 1:
                try:
                    pointer = tape.index(0, pointer)
                except ValueError:
                    raise RuntimeError("Pointer moved past end of tape") from None
            elif step == -1:
                try:
                    pointer = tape.rindex(0, 0, pointer + 1)
                except ValueError:
                    raise RuntimeError("Pointer moved below 0") from None
            else:
                while tape[pointer] != 0:
                    pointer += step
                    if pointer < 0:
                        raise RuntimeError("Pointer moved below 0")
                    if pointer >= tape_size:
                        raise RuntimeError("Pointer moved past end of tape")

        elif operation == OUTPUT:
            out.write(bytes((tape[pointer],)))

        elif operation == INPUT:
            character = inp.read(1)
            if character:
                tape[pointer] = character[0]

        else:
            raise RuntimeError(f"Unknown opcode {operation!r}")

        program_counter += 1
