from blocks_world.blocks import State, blocks_outside_first_stack, are_blocks_sorted_on_one_stack, blocks_sorted_on_first_stack

if __name__ == '__main__':
    h = []
    i = 0
    s = State(
        final_check=are_blocks_sorted_on_one_stack,
        heuristics=[blocks_outside_first_stack, blocks_sorted_on_first_stack],
        layout=[[1, 2, 5], [3, 4, 8, 7], [6, 9]],
    )
    print(s, end="".join(["=" for _ in range(16)] + ["\n\n"]))

    G = [s]
    Z = []
    while len(G) > 0:
        if s.is_final():
            break

        for child in s.sprout():
            if child not in Z:
                G.append(child)
        G.remove(s)
        i = i + 1

        for state in G:
            h.append(state.cost + state.heuristic())

        m = min(h)
        m = h.index(m)
        s = G[m]
        Z.append(s)
        h.clear()
        print('iteracja: ', i, '\n')
        print(s)