from functools import reduce

from blocks_world.model import State


def blocks_outside_first_stack(stacks: State.STACKS_TYPE) -> int:
    return reduce(lambda a, b: a + len(b), stacks, 0) - len(stacks[0])


def misplaced_blocks(stacks: State.STACKS_TYPE) -> int:
    h = 2 * sum(len(stack) for stack in stacks) - len(stacks[0])
    stack = stacks[0]
    for i in range(len(stack)):
        if stack[i] != i:
            h += 3
    return h


def estimate_moves(stacks: State.STACKS_TYPE) -> int:
    h = 0
    """ first stack """
    stack = stacks[0]

    for i in range(len(stack)):

        if stack[i] == i:  # block placed well
            continue

        elif stack[i] < i:  # case when block is above its target
            h = h + (len(stack) - stack[i]) + 1

        elif stack[i] > i:  # case when block is below its target
            h = h + (len(stack) - i) + stack[i] - i + 1

    """ other stacks """
    for i in range(len(stacks)):

        if i == 0:  # start from the second stack
            continue

        stack = stacks[i]

        for j in range(len(stack)):  # go through all stacks

            if len(stacks[0]) > stack[j]:  # position of our blocks is taken
                h = h + len(stacks[0]) - stack[j] + len(stack) - j
            elif len(stacks[0]) < stack[j]:  # lacks some block below our position
                h = h + len(stack) - j

    return 4 * h
