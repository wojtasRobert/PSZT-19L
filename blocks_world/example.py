from blocks_world.blocks import State, blocks_outside_first_stack, best_heuristic_ever, misplaced_blocks
from blocks_world.a_star import a_star

if __name__ == '__main__':
    BLOCKS = 6
    STACKS = 3

    start_state = State(
        layout=State.gen_layout(BLOCKS, STACKS),
        heuristics=[misplaced_blocks, best_heuristic_ever],
    )
    print(start_state, end="".join(["=" for _ in range(16)] + ["\n\n"]))

    # for state in start_state.sprout():
    #     print('h = ', state.heuristic(), '\n')
    #     # print(state)

    final_s, i = a_star(start_state, State([list(range(BLOCKS))]))
    print(final_s)
    print("Iterations:", i)
    print("Steps:", final_s.cost)
