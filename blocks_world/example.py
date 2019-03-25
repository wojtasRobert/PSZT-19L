from blocks_world.blocks import State, blocks_outside_first_stack, are_blocks_sorted_on_one_stack

if __name__ == '__main__':
    s = State(
        final_check=are_blocks_sorted_on_one_stack,
        heuristics=[blocks_outside_first_stack],
        layout=[[1, 2, 5], [3, 4], [6]],
    )
    print(s, end="".join(["=" for _ in range(16)] + ["\n\n"]))
    for state in s.sprout():
        print(state)
