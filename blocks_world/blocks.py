from copy import deepcopy
from functools import reduce
from itertools import chain
from typing import List, Callable
from random import shuffle, randrange


class State:
    BLOCK_PADDING = 2
    TABLE_PADDING = 1
    FINAL_TEXT = "FINAL"

    STACKS_TYPE = List[List[int]]
    FINAL_CHECK_TYPE = Callable[[STACKS_TYPE], bool]
    HEURISTIC_TYPE = Callable[[STACKS_TYPE], int]
    HEURISTICS_TYPE = List[Callable[[STACKS_TYPE], int]]

    final_check: FINAL_CHECK_TYPE
    heuristics: HEURISTICS_TYPE
    stacks: STACKS_TYPE

    def __init__(
            self,
            final_check: FINAL_CHECK_TYPE,
            heuristics: HEURISTICS_TYPE,
            layout: STACKS_TYPE = None,
            cost: int = 0,
    ):
        self.final_check = final_check
        self.heuristics = heuristics
        self.cost = cost

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
                "-" for _ in range(
                    max(
                        len(self.stacks) * (max_digits + self.BLOCK_PADDING) + self.TABLE_PADDING,
                        len(self.FINAL_TEXT) + 2 * self.TABLE_PADDING,
                    )
                )
            ] + [
                ("\n" + "".join(" " for _ in range(self.TABLE_PADDING)) + self.FINAL_TEXT + "\n")
                if self.is_final() else "\n"
            ])

    def __eq__(self, other) -> bool:
        return sorted(self.stacks) == sorted(other.stacks)

    def __lt__(self, other):
        return self.cost + self.heuristic() < other.cost + other.heuristic()

    def heuristic(self):
        """
        Calculates the value of the heuristic function for the state.
        """
        # TODO: take all heuristics into account, not just the first
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

    def copy(self):
        """
        Makes a deep copy of the state.
        """
        return State(self.final_check, self.heuristics, deepcopy(self.stacks), self.cost)

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

    def is_final(self):
        """
        Checks if the state is final by executing its final_check function.
        """
        return self.final_check(self.stacks)

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


def blocks_outside_first_stack(stacks: State.STACKS_TYPE) -> int:
    return sum(len(stack) for stack in stacks) - len(stacks[0])


def blocks_sorted_on_first_stack(stacks: State.STACKS_TYPE):  # -> int:
    stack = stacks[0]
    h = 0
    for i in range(len(stack)):
        if stack[i] == i+1:
            continue
        h = 9 - i
        break
    return h


def are_blocks_sorted_on_one_stack(stacks: State.STACKS_TYPE, reverse=False) -> bool:
    if len(stacks) != 1:
        return False
    stack = stacks[0]
    return stack == sorted(stack, reverse=reverse)
