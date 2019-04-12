# This script can be used to generate a table that shows algorithm's performance.
# You can run it by executing `python3 -m blocks_world.analysis`.

from statistics import mean, stdev
from sys import stderr
from concurrent.futures import ProcessPoolExecutor, as_completed

from blocks_world.model import State
from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.heuristics import estimate_moves, misplaced_blocks, blocks_outside_biggest_stack, unsorted_biggest_stack_blocks


def do_analysis(blocks, stacks, each):
    iterations = []
    costs = []
    costs_over_iterations = []

    fails = 0
    for _ in range(each):
        initial_state = State(
            layout=State.gen_layout(blocks, stacks),
            heuristics=[misplaced_blocks],
        )
        try:
            final_state, it = a_star(
                state=initial_state,
                final=initial_state.make_final(),
                max_iterations=1000,
            )
            iterations.append(it)
            costs.append(final_state.cost)
            costs_over_iterations.append(final_state.cost / it)
        except TooManyIterations:
            fails += 1
    return (
        blocks,
        stacks,
        mean(iterations),
        stdev(iterations),
        mean(costs),
        stdev(costs),
        100 * mean(costs_over_iterations),
        100 * fails / EACH,
    )


if __name__ == '__main__':
    EACH = 100
    MAX_BLOCKS = 6
    DIAGONAL_ONLY = False

    with ProcessPoolExecutor(max_workers=12) as executor:
        future_to_result = {}

        for blocks in range(1, MAX_BLOCKS + 1):
            for stacks in range(1, blocks + 1):
                if DIAGONAL_ONLY and blocks != stacks:
                    continue
                future_to_result[executor.submit(do_analysis, blocks, stacks, EACH)] = (blocks, stacks)

        results = []

        for future in as_completed(future_to_result):
            print("{:.2f}%".format(100 * (len(results) + 1) / len(future_to_result)), file=stderr)
            blocks, stacks = future_to_result[future]
            results.append("{:7d} {:7d} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f}".format(
                *future.result()
            ))

        print("{:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s}"
              .format("BLOCKS", "STACKS", "AVGIT", "STDIT", "AVGCOST", "STDCOST", "CTOVRIT%", "FAILS%"))
        for result in sorted(results):
            print(result)
