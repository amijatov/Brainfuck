from clearloop import rewrite_clear_loops
from forward import forward
from backward import backwards
from multiply import rewrite_multiply_loops
from peephole import peephole
from scanloop import rewrite_scan_loops


MAX_ROUNDS = 4
PASSES = ("clear", "multiply", "forward", "peephole", "scan", "backwards")


def _one_round(instructions, passes):
    """Führt die aktivierten Optimierungspässe einmal in fester Reihenfolge aus."""
    if "clear" in passes:
        instructions = rewrite_clear_loops(instructions)
    if "multiply" in passes:
        instructions = rewrite_multiply_loops(instructions)
    if "forward" in passes:
        instructions = forward(instructions)
    if "peephole" in passes:
        instructions = peephole(instructions)
    if "scan" in passes:
        instructions = rewrite_scan_loops(instructions)
    if "backwards" in passes:
        instructions = backwards(instructions)
    return instructions


def optimize_bf(instructions, passes=None, max_rounds=MAX_ROUNDS):
    """Wiederholt die Optimierung bis zur Stabilität oder zur Rundengrenze."""
    passes = set(PASSES) if passes is None else set(passes)
    unknown = passes - set(PASSES)
    if unknown:
        raise ValueError(
            f"unknown pass(es): {sorted(unknown)}; known passes are {list(PASSES)}"
        )

    original = instructions
    try:
        for _ in range(max_rounds):
            previous = instructions
            instructions = _one_round(instructions, passes)
            if instructions == previous:
                break
        return instructions
    except RecursionError:
        return original
