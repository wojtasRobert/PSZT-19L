from blocks_world.blocks import State, blocks_outside_first_stack, are_blocks_sorted_on_one_stack
from blocks_world.a_star import a_star

if __name__ == '__main__':
    start_state = State(
        final_check=are_blocks_sorted_on_one_stack,
        heuristics=[blocks_outside_first_stack],
        layout=State.gen_layout(blocks=5, stacks=3),
    )
    print(start_state, end="".join(["=" for _ in range(16)] + ["\n\n"]))
    final_s, i = a_star(start_state)
    print(final_s)
    print("Iterations:", i)
    print("Steps:", final_s.cost)
