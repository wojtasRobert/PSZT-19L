from unittest import TestCase

from .blocks import State


class TestBlocks(TestCase):
    def test_heuristics(self):
        self.assertEqual(State(heuristics=[lambda s: 0]).heuristic(), 0)
        self.assertEqual(State(heuristics=[lambda s: 42]).heuristic(), 42)
        self.assertEqual(State(heuristics=[lambda s: 42, lambda s: 40]).heuristic(), 42)
        self.assertEqual(State(heuristics=[lambda s: 32, lambda s: 35]).heuristic(), 35)

    def test_move(self):
        state = State([[1, 2, 3], [4, 5, 6]])

        state.move(0, -1)
        self.assertEqual([[1, 2], [4, 5, 6], [3]], state.stacks)

        state.move(2, 0)
        self.assertEqual([[1, 2, 3], [4, 5, 6]], state.stacks)

        self.assertRaises(IndexError, state.move, 2, 0)

        self.assertEqual([[1, 2, 3], [4, 5, 6]], state.stacks)

        state.move(1, 0)
        self.assertEqual([[1, 2, 3, 6], [4, 5]], state.stacks)
