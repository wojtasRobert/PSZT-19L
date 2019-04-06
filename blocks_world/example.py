from blocks import State, blocks_outside_first_stack, are_blocks_sorted_on_one_stack, best_heuristic_ever, misplaced_blocks
from a_star import a_star

if __name__ == '__main__':
    start_state = State(
        final_check=are_blocks_sorted_on_one_stack,
        heuristics=[misplaced_blocks, best_heuristic_ever],
        layout=State.gen_layout(blocks=6, stacks=3),
    )
    print(start_state, end="".join(["=" for _ in range(16)] + ["\n\n"]))

    # for state in start_state.sprout():
    #     print('h = ', state.heuristic(), '\n')
    #     # print(state)

    final_s, i = a_star(start_state)
    print(final_s)
    print("Iterations:", i)
    print("Steps:", final_s.cost)
