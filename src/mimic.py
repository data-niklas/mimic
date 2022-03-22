import argparse
import pathlib

from play import Play
from record import Record

NAME = "mimic"
VERSION = "1.0.0"
AUTHOR = "data-niklas"
DESCRIPTION = "Mimic user input"

def create_argparser():
    parser = argparse.ArgumentParser(description=DESCRIPTION, prog=NAME)
    parser.add_argument('action', choices=["play", "record"])
    parser.add_argument('file', type=pathlib.Path)
    return parser

if __name__ == "__main__":
    parser = create_argparser()
    args = parser.parse_args()
    file = args.file
    action = args.action

    if action == "play":
        play = Play()
        play.run_file(file, dict())
    
