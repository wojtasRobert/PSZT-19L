from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.blocks import State, best_heuristic_ever, misplaced_blocks

if __name__ == '__main__':
    BLOCKS = 6
    STACKS = 3

    start_state = State(
        layout=State.gen_layout(BLOCKS, STACKS),
        heuristics=[misplaced_blocks, best_heuristic_ever],
    )

    # for state in start_state.sprout():
    #     print('h = ', state.heuristic(), '\n')
    #     # print(state)

    try:
        final_s, i = a_star(start_state, State([list(range(BLOCKS))]))
        final_s.print_backtrace()
        print("Iterations:", i)
        print("Steps:", final_s.cost)
    except TooManyIterations:
        print("Too many iterations")
        exit(1)
