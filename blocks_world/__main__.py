from argparse import ArgumentParser
from ast import literal_eval
from sys import stderr

from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.heuristics import *
from blocks_world.model import State

parser = ArgumentParser(
    description="Solve a given blocks world problem.",
)

parser.add_argument(
    '--initial',
    '-i',
    type=str,
    help="How blocks are initially arranged into stacks. Ex. [[2,1,3],[4]]. The inner lists are stacks.",
)
parser.add_argument(
    '--random', '-r',
    action='store_true',
    help="Random initial state. (see --blocks and --stacks)",
)
parser.add_argument(
    '--blocks', '-b',
    type=int,
    help="The number of blocks (used with --random).",
)
parser.add_argument(
    '--stacks', '-s',
    type=int,
    help="The number of stacks (used with --random).",
)
parser.add_argument(
    '-v',
    action='store_true',
    help="If set, initial state will be displayed.",
)
parser.add_argument(
    '--verbose', '-vv',
    action='store_true',
    help="If set, every state in the solution will be displayed along with other extra info.",
)
parser.add_argument(
    '--iterations', '-it',
    type=int,
    default=500,
    help="Maximum number of iterations.",
)
HEURISTICS = {
    0: [blocks_outside_biggest_stack, unsorted_biggest_stack_blocks, move_once_or_twice],
    1: [blocks_outside_biggest_stack],
    2: [unsorted_biggest_stack_blocks],
    3: [move_once_or_twice],
}
HEURISTICS_HELP = "0 -- deafult, max of all heuristics; " \
                  "1 -- blocks_outside_biggest_stack; " \
                  "2 -- unsorted_biggest_stack_blocks; " \
                  "3 -- move_once_or_twice"
parser.add_argument(
    '--heuristics', '-he',
    type=int,
    default=0,
    help="Choose heuristics used for the calculations." + HEURISTICS_HELP
)

args = parser.parse_args()

initial = literal_eval(args.initial) if args.initial else None

if not (args.initial or args.random) or (args.initial and args.random):
    print("You need to pass --initial or --random (but not both).", file=stderr)
    exit(1)

if args.initial and (args.blocks or args.stacks):
    print("--blocks and --stacks have to be passed only when --random is passed.", file=stderr)
    exit(1)

if args.random and not (args.blocks and args.stacks):
    print("If --random was passed, also --blocks and --stacks have to be passed.", file=stderr)
    exit(1)

if args.verbose and args.v:
    print("You can only choose one verbosity level: -v or -vv.", file=stderr)
    exit(1)

if args.random and not (args.v or args.verbose):
    print(
        "Passing --random without passing -v or -vv makes no sense, "
        "because you will not be able to see the initial state.",
        file=stderr
    )
    exit(1)
if args.heuristics >= len(HEURISTICS):
    print("--heuristics out of range, see --help", file=stderr)
    exit(1)

start_state = State(
    layout=State.gen_layout(args.blocks, args.stacks) if args.random else initial,
    heuristics=HEURISTICS[args.heuristics],
)

terminal_state = start_state.make_final()

try:
    final_s, i = a_star(
        state=start_state,
        final=terminal_state,
        max_iterations=args.iterations,
    )
    if args.v:
        print(start_state)
    elif args.verbose:
        final_s.print_backtrace(print_states=True)
        print("Iterations:", i, file=stderr)
        print("Steps:", final_s.cost, file=stderr)
    if not args.verbose:
        final_s.print_backtrace()
        print()
    if args.v:
        print(final_s)

except TooManyIterations:
    print("Too many iterations, try increasing the default limit (500) with --iterations flag.", file=stderr)
    exit(1)
