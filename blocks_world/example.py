from blocks_world.blocks import State, blocks_outside_first_stack

if __name__ == '__main__':
    s = State([blocks_outside_first_stack], [[1, 2, 5], [3, 4], [6]])
    print(s, end="".join(["=" for _ in range(16)] + ["\n\n"]))
    for state in s.sprout():
        print(state)
