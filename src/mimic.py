import argparse
import pathlib

from play import PlayController
from record import Record

NAME = "mimic"
VERSION = "1.0.0"
AUTHOR = "data-niklas"
DESCRIPTION = "Mimic user input"

def create_argparser():
    parser = argparse.ArgumentParser(description=DESCRIPTION, prog=NAME)
    parser.add_argument('action', choices=["play", "record"])
    parser.add_argument('file', type=pathlib.Path)
    parser.add_argument('--vars', nargs='+', required=False)
    return parser


def parse_variables(var_args):
    variables = dict()
    if var_args is None:
        return variables
    for var_arg in var_args:
        if not '=' in var_arg:
            # TODO error
            pass
        parts = var_arg.split('=')
        if len(parts) > 2:
            # TODO error
            pass
        variables[parts[0]] = parts[1]

    return variables

if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()
    file = args.file
    action = args.action

    if action == "play":
        play_controller = PlayController()
        variables = parse_variables(args.vars)
        play_controller.run_file(file, variables)
