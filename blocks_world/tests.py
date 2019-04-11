from functools import reduce
from unittest import TestCase

from blocks_world.a_star import a_star
from blocks_world.heuristics import estimate_moves, misplaced_blocks
from blocks_world.model import State


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


class TestAStar(TestCase):
    def test_simple(self):
        self._test_layout([[0]])
        self._test_layout([[0, 1, 2, 3]])
        self._test_layout([[3, 2, 1, 0]])

    def _test_layout(self, layout):
        initial = State(
            layout=layout,
            heuristics=[misplaced_blocks, estimate_moves],
        )
        final = State([sorted(reduce(lambda a, b: a + b, initial.stacks, []))])

        r_final, _ = a_star(initial, final)

        self.assertTrue(r_final == final)
