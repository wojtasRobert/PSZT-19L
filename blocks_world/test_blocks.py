from unittest import TestCase

from .blocks import State


class TestBlocks(TestCase):
    def test_heuristics(self):
        self.assertEqual(State(None, [lambda s: 0]).heuristic(), 0)
        self.assertEqual(State(None, [lambda s: 42]).heuristic(), 42)
        self.assertEqual(State(None, [lambda s: 42, lambda s: 40]).heuristic(), 42)
        self.assertEqual(State(None, [lambda s: 32, lambda s: 35]).heuristic(), 35)
