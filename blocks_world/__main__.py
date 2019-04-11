from argparse import ArgumentParser
from ast import literal_eval
from functools import reduce
from sys import stderr

from blocks_world.a_star import a_star, TooManyIterations
from blocks_world.heuristics import best_heuristic_ever, misplaced_blocks
from blocks_world.model import State

parser = ArgumentParser(
    description="Solve a given blocks world problem.",
)

parser.add_argument(
    '--initial',
    '-i',
    type=str,
    help="How blocks are initially arranged into stacks. Ex. [[2, 1, 3], [4]]. The inner lists are stacks.",
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
    default=300,
    help="Maximum number of iterations.",
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

start_state = State(
    layout=State.gen_layout(args.blocks, args.stacks) if args.random else initial,
    heuristics=[misplaced_blocks, best_heuristic_ever],
)

# Count blocks
terminal_state = None
if args.blocks:
    terminal_state = State([list(range(args.blocks))])
else:
    terminal_state = State([sorted(reduce(lambda a, b: a + b, start_state.stacks, []))])

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
    print("Too many iterations", file=stderr)
    exit(1)
