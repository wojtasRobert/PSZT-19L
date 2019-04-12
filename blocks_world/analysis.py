from statistics import mean, stdev
from sys import stderr
from concurrent.futures import ProcessPoolExecutor, as_completed

from blocks_world.model import State
from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.heuristics import estimate_moves, misplaced_blocks


def do_analysis(blocks, stacks, each):
    iterations = []
    costs = []
    costs_over_iterations = []

    fails = 0
    for _ in range(EACH):
        initial_state = State(
            layout=State.gen_layout(blocks, stacks),
            heuristics=[misplaced_blocks, estimate_moves],
        )
        try:
            final_state, it = a_star(
                state=initial_state,
                final=initial_state.make_final(),
                max_iterations=400,
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
    EACH = 500

    print("{:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s} {:>7s}"
          .format("BLOCKS", "STACKS", "AVGIT", "STDIT", "AVGCOST", "STDCOST", "CTOVRIT%", "FAILS%"))

    with ProcessPoolExecutor(max_workers=12) as executor:
        future_to_result = {}

        for blocks in range(2, 7):
            for stacks in range(1, blocks + 1):
                future_to_result[executor.submit(do_analysis, blocks, stacks, EACH)] = (blocks, stacks)

        results = []

        for future in as_completed(future_to_result):
            print(blocks, stacks, file=stderr)
            blocks, stacks = future_to_result[future]
            results.append("{:7d} {:7d} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.2f} {:7.0f}".format(
                *future.result()
            ))

        for result in sorted(results):
            print(result)