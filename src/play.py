from pynput.mouse import Controller as MouseController
from pynput.keyboard import Controller as KeyboardController

from ast import *

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
            line = self.line().strip()
            self.advance()
            if line.startswith("-"):
                return header
            else:
                header.add_variable(line)

        return header

    def parse_if(self):
        condition = self.line().strip()[2:]
        self.advance()
        block = self.parse_block()
        if self.line().strip() == "else":
            self.advance()
            else_block = self.parse_block()
        else:
            else_block = Body()
        return If(condition, block, else_block)


    def parse_loop(self):
        n = self.line().strip()[5:]
        self.advance()
        block = self.parse_block()
        return Loop(n, block)

    def parse_move(self, millis, line):
        line = line[5:]
        parts = line.split(' ')
        if len(parts) >= 2:
            x = parts[0]
            y = parts[1]
            relative = "true"
        if len(parts) == 3:
            relative = parts[2]
        # TODO throw error

        return Move(millis, x, y, relative)

    def parse_click(self, millis, line):
        line = line[6:]
        parts = line.split(' ')
        if len(parts) >= 1:
            button = parts[0]
            times = "1"

        if len(parts) == 2:
            times = parts[1]

        return Click(millis, button, times)


    def parse_key(self, millis, line):
        line = line[4:]
        parts = line.split(' ')
        if len(parts) == 2:
            key = parts[0]
            is_down = parts[1]

        return Key(millis, key, is_down)


    def parse_type(self, millis, line):
        line = line[5:]
        return Type(millis, line)

    def parse_scroll(self, millis, line):
        line = line[7:]
        parts = line.split(' ')
        if len(parts) == 2:
            x = parts[0]
            y = parts[1]

        return Scroll(millis, x, y)

    def parse_command(self, millis, line):
        line = line[8:]
        return Command(millis, line)

    def parse_action(self):
        line = self.line().strip()
        millis_index = line.index(" ")
        millis = line[:millis_index]
        line = line[millis_index+1:].lstrip()
        if line.startswith("move"):
            return self.parse_move(millis, line)
        elif line.startswith("click"):
            return self.parse_click(millis, line)
        elif line.startswith("key"):
            return self.parse_key(millis, line)
        elif line.startswith("type"):
            return self.parse_type(millis, line)
        elif line.startswith("scroll"):
            return self.parse_scroll(millis, line)
        elif line.startswith("command"):
            return self.parse_command(millis, line)
        else:
            print(f"Unknown action {line}")
        return 1


    def parse_block(self):
        body = Body()
        while not self.is_eof():
            line = self.line().strip()
            if line == "end":
                self.advance()
                return body
            elif line == "else":
                return body
            elif line.startswith("if"):
                part = self.parse_if()
            elif line.startswith("loop"):
                part = self.parse_loop()
            else:
                part = self.parse_action()
                self.advance()
            
            body.add_part(part)

        return body

    def parse(self, lines):
        self.reset()
        self.lines = lines
        fragment = Fragment()
        fragment.header = self.parse_header()
        fragment.body = self.parse_block()
        print(fragment.__str__())

        return fragment

class Play():
    def __init__(self, controller, variables):
        self.controller = controller
        self.variables = variables

    def var_or_val(self, name):
        if name.startswith("$"):
            return self.variables[name[1:]]
        else:
            return name

class PlayController():
    def __init__(self) -> None:
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
        self.parser = Parser()

    def run_file(self, file, variables):
        file_handle = open(file, 'r')
        lines = file_handle.readlines()
        # TODO check all vars
        fragment = self.parser.parse(lines)
        fragment(Play(self, variables))
        file_handle.close()

