from copy import deepcopy
from functools import reduce
from itertools import chain
from random import shuffle, randrange
from typing import List, Callable


class State:
    BLOCK_PADDING = 2
    TABLE_PADDING = 1

    STACKS_TYPE = List[List[int]]
    HEURISTIC_TYPE = Callable[[STACKS_TYPE], int]
    HEURISTICS_TYPE = List[Callable[[STACKS_TYPE], int]]

    heuristics: HEURISTICS_TYPE
    stacks: STACKS_TYPE

    def __init__(
            self,
            layout: STACKS_TYPE = None,
            heuristics: HEURISTICS_TYPE = None,
            cost: int = 0,
            parent=None,
    ):
        self.heuristics = heuristics
        self.cost = cost
        self.parent = parent
        self.operator = None

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

    def __eq__(self, other) -> bool:
        return sorted(self.stacks) == sorted(other.stacks)

    def __lt__(self, other):
        return self.cost + self.heuristic() < other.cost + other.heuristic()

    def heuristic(self):
        """
        Calculates the value of the heuristic function for the state.
        """
        if self.heuristics is None:
            return 0

        return max(h(self.stacks) for h in self.heuristics)

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
        self.operator = [source, destination]

    def copy(self):
        """
        Makes a deep copy of the state.
        """
        return State(deepcopy(self.stacks), self.heuristics, self.cost, self)

    def sprout(self):
        """
        Makes a list of every possible state, resulting from the state.
        """
        states = []

        for source in range(len(self.stacks)):
            for destination in range(-1, len(self.stacks)):
                if source == destination:
                    continue
                if len(self.stacks[source]) == 1 and destination == -1:
                    # don't create a new stack from a stack that has only one block
                    continue
                state = self.copy()
                state.move(source, destination)
                state.cost += 1
                states.append(state)

        return states

    def print_backtrace(self, print_states=False):
        backtrace = [self]

        while backtrace[-1].parent is not None:
            backtrace.append(backtrace[-1].parent)

        for state in reversed(backtrace):
            if state.operator:
                print("{} -> {}".format(*state.operator))
            if print_states:
                print(str(state))

    def _level_to_str(self, level, max_digits):
        return "".join(str(stack[level] if level < len(stack) else "")
                       .rjust(max_digits + self.BLOCK_PADDING) for stack in self.stacks)

    @staticmethod
    def gen_layout(blocks, stacks):
        block_sequence = list(range(blocks))
        shuffle(block_sequence)

        layout = [[block_sequence.pop()] for _ in range(stacks)]
        for _ in range(len(block_sequence)):
            layout[randrange(stacks)].append(block_sequence.pop())

        return layout
