from functools import reduce

from blocks_world.model import State


def blocks_outside_biggest_stack(stacks: State.STACKS_TYPE) -> int:
    return reduce(lambda a, b: a + len(b), stacks, 0) - len(max(stacks, key=lambda x: len(x)))


def unsorted_biggest_stack_blocks(stacks: State.STACKS_TYPE) -> int:
    largest = max(stacks, key=lambda x: len(x))
    sorted_first = sorted(largest)

    unsorted_blocks = 0
    for idx in range(min(len(sorted_first), len(stacks))):
        if sorted_first[idx] != largest[idx]:
            unsorted_blocks += 1

    unsorted_blocks += max(0, len(stacks[0]) - len(sorted_first))

    return unsorted_blocks


def move_once_or_twice(stacks: State.STACKS_TYPE) -> int:
    h1 = 0
    h2 = 0

    """ biggest stack """
    largest = max(stacks, key=lambda x: len(x))

    for i in range(len(largest)):
        if largest[i] != i:
            h2 = len(largest) - i
            break

    """ other stacks """
    for stack in stacks:
        if stack == largest:
            continue

        for j in range(len(stack)):
            if j == 0:
                h1 += 1

            if stack[j] > stack[j-1]:
                h2 += 1
            else:
                h1 += 1

    return h1 + h2
