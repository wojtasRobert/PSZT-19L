# This is an example script that shows the usage of this module.
# You can run it by executing `python3 -m blocks_world.example`.
# One can try to experiment by changing `BLOCKS` and `STACKS` below
# to change the parameters of random problem generation.

from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.heuristics import *
from blocks_world.model import State

if __name__ == '__main__':
    BLOCKS = 6
    STACKS = 3

    start_state = State(
        layout=State.gen_layout(BLOCKS, STACKS),
        heuristics=[blocks_outside_biggest_stack, unsorted_biggest_stack_blocks, move_once_or_twice],
    )

    try:
        final_s, i = a_star(start_state, State([list(range(BLOCKS))]), step=False)
        final_s.print_backtrace(print_states=True)
        print("Iterations:", i)
        print("Steps:", final_s.cost)
    except TooManyIterations:
        print("Too many iterations")
        exit(1)
