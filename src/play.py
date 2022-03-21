from pynput.mouse import MouseController
from pynput.keyboard import KeyboardController

from .ast import *

class Parser():
    def __init__(self) -> None:
        self.reset()

    def reset(self):
        self.i = 0

    def line(self):
        return self.lines[self.i]

    def is_eof(self):
        return self.i >= len(self.lines)

    def line_is_comment(self):
        return self.line().startswith("#")

    def skip_comments(self):
        while not self.is_eof() and self.line_is_comment():
            self.i = self.i + 1

    def advance(self):
        self.i = self.i + 1
        self.skip_comments()

    def parse_header(self):
        self.skip_comments()
        header = Header()
        while not self.is_eof():
            line = self.line().trim()
            self.advance()
            if line.startswith("-"):
                return header
            else:
                header.add_variable(line)

        return header

    def parse_if(self):
        condition = self.line().trim()[2:]
        block = self.parse_block()
        if self.line().trim() == "else":
            self.advance()
            else_block = self.parse_block()
        else:
            else_block = Body()
        return If(condition, block, else_block)


    def parse_loop(self):
        n = self.line().trim()[5:]
        block = self.parse_block()
        return Loop(n, block)

    def parse_move(self):
        line = self.line().trim()[5:]
        parts = line.split(' ')
        if len(parts) >= 2:
            x = parts[0]
            y = parts[1]
            relative = True
        if len(parts) == 3:
            relative = parts[2]
        # TODO throw error

        return Move(x, y, relative)


    def parse_block(self):
        body = Body()
        while not self.is_eof():
            line = self.line().trim()
            if line == "end":
                self.advance()
                return body
            elif line == "else":
                return body
            elif line.startswith("if"):
                part = self.parse_if()
            elif line.startswith("loop"):
                part = self.parse_loop()
            elif line.startswith("move"):
                part = self.parse_move()
            
            body.add_part(part)

        return body

    def parse(self, lines):
        self.reset()
        self.lines = lines
        fragment = Fragment()
        fragment.header = self.parse_header()
        fragment.body = self.parse_block()

        return fragment


class Play():
    def __init__(self) -> None:
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        self.variables = dict()
        self.parser = Parser()

    def run_file(self, file, variables):
        self.variables = variables
        file_handle = open(file, 'r')
        lines = file_handle.readlines()
        fragment = self.parser.parse(lines)
        fragment(self)
        file_handle.close()

    def var_or_val(self, name):
        if name.startswith("$"):
            return self.variables[name[1:]]
        else:
            return name