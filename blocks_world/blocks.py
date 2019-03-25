from copy import deepcopy
from functools import reduce
from itertools import chain
from typing import List, Callable


class State:
    BLOCK_PADDING = 2
    TABLE_PADDING = 1
    heuristics: List[Callable[[List[List[int]]], int]]
    stacks: List[List[int]]

    def __init__(self, heuristics: List[Callable[[List[List[int]]], int]], layout: List[List[int]] = None):
        self.heuristics = heuristics

        if layout is None:
            layout = []
        self.stacks = layout

    def __str__(self):
        max_digits = len(str(max(chain.from_iterable(self.stacks))))
        max_stack_height = len(max(self.stacks, key=lambda x: len(x)))

        return "".join(
            [reduce(
                lambda previous, current: "".join([previous, self._level_to_str(current, max_digits), "\n"]),
                reversed(range(max_stack_height)),
                "",
            )] + [
                "-" for _ in range(len(self.stacks) * (max_digits + self.BLOCK_PADDING) + self.TABLE_PADDING)
            ] + [
                "\n"
            ])

    def heuristic(self):
        """
        Calculates the value of the heuristic function for a state.
        """
        # TODO: take all heuristics into account, not just the first
        return self.heuristics[0](self.stacks)

    def move(self, source, destination):
        """
        Moves a block from one stack to another stack IN PLACE.
        :param source: the index of source stack
        :param destination: the index of destination stack or -1 to create a new stack
        """
        block = self.stacks[source].pop()
        if destination == -1:
            self.stacks.append([block])
        else:
            self.stacks[destination].append(block)
        if not self.stacks[source]:
            del self.stacks[source]

    def copy(self):
        """
        Makes a deep copy of a state.
        """
        return State(self.heuristics, deepcopy(self.stacks))

    def sprout(self):
        """
        Makes a list of every possible state, resulting from a state.
        """
        states = []

        for source in range(len(self.stacks)):
            for destination in range(-1, len(self.stacks)):
                if source == destination:
                    continue
                state = self.copy()
                state.move(source, destination)
                states.append(state)

        return states

    def _level_to_str(self, level, max_digits):
        return "".join(str(stack[level] if level < len(stack) else "")
                       .rjust(max_digits + self.BLOCK_PADDING) for stack in self.stacks)


def blocks_outside_first_stack(stacks: List[List[int]]):
    return sum(len(stack) for stack in stacks) - len(stacks[0])
