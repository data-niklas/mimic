from pynput.mouse import Listener as MouseListener
from pynput.keyboard import Listener as KeyboardListener, GlobalHotKeys
from time import time_ns

from ast import *

from utils import parse_key, parse_button

class Record():
    def __init__(self):
        self.stopped = False


    def add_part(self, part):
        self.fragment.body.add_part(part)

    def new_action(self):
        current_time = time_ns()
        delta = current_time - self.last_action_time
        self.last_action_time = current_time
        return str(int(round(delta / 1000000)))

    def record_to_file(self, file, exit_hotkey):
        self.fragment = Fragment()
        self.file = file

        def on_move(x, y):
            delta = self.new_action()
            part = Move(delta, str(x), str(y), "false")
            self.add_part(part)
            if self.stopped:
                return False

        def on_click(x, y, button, pressed):
            if not pressed:
                return
            delta = self.new_action()
            part = Click(delta, parse_button(button), "1")
            self.add_part(part)

        def on_scroll(x, y, dx, dy):
            delta = self.new_action()
            part = Scroll(delta, str(dx), str(dy))
            self.add_part(part)

        def on_press(key):
            print(key)
            delta = self.new_action()
            key = parse_key(key)
            part = Key(delta, key, "true")
            self.add_part(part)

        def on_release(key):
            delta = self.new_action()
            key = parse_key(key)
            part = Key(delta, key, "false")
            self.add_part(part)
            if self.stopped:
                return False


        def on_exit():
            self.mouse_listener.stop()
            self.stop()
            return False

        self.mouse_listener = MouseListener(
           on_move=on_move,
           on_click=on_click,
           on_scroll=on_scroll
        )
        self.keyboard_listener = KeyboardListener(
           on_press=on_press,
           on_release=on_release
        )
        self.hotkeys = GlobalHotKeys({
            exit_hotkey: on_exit
        })

        self.last_action_time = time_ns()
        self.mouse_listener.start()
        self.keyboard_listener.start()
        self.hotkeys.start()


    def join(self):
        # self.mouse_listener.join()
        # self.keyboard_listener.join()
        self.hotkeys.join()


    def stop(self):
        self.stopped = True
        self.mouse_listener.stop()
        self.keyboard_listener.stop()
        self.hotkeys.stop()
        self.write_fragment()


    def write_fragment(self):
        with open(self.file, 'w') as file:
            file.write(str(self.fragment))
