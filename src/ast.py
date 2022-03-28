import subprocess
from pynput.mouse import Button
from pynput.keyboard import Key as PynputKey
from time import sleep

class Header():
    def __init__(self) -> None:
        self.variables = []

    def add_variable(self, variable: str) -> None:
        self.variables.append(variable)

    def __str__(self) -> str:
        return "\n".join(self.variables)


class Part():
    def __call__(self, instance):
        pass

class Body():
    def __init__(self) -> None:
        self.parts = []

    def add_part(self, part: Part) -> None:
        self.parts.append(part)

    def __call__(self, instance):
        for part in self.parts:
            part(instance)

    def __str__(self) -> str:
        return "\n".join([str(part) for part in self.parts])


class Fragment():
    def __init__(self) -> None:
        self.header = Header()
        self.body = Body()

    def __call__(self, instance):
        self.body(instance)

    def __str__(self) -> str:
        return f"{self.header}\n-\n{self.body}"



class If(Part):
    def __init__(self, condition, body, else_body) -> None:
        self.condition = condition
        self.body = body
        self.else_body = else_body

    def __call__(self, instance):
        exit_code, _ = subprocess.getstatusoutput(instance.var_or_val(self.condition))
        if exit_code == 0:
            self.body(instance)
        else:
            self.else_body(instance)

    def __str__(self) -> str:
        return f"if {self.condition}\n{self.body}\nend\nelse\n{self.else_body}\nend"

class Loop(Part):
    def __init__(self, n, body) -> None:
        self.n = n
        self.body = body

    def __call__(self, instance):
        n = int(instance.var_or_val(self.n))
        for _ in range(n):
            self.body(instance)

    def __str__(self) -> str:
        return f"loop {self.n}\n{self.body}\nend"

class TimedPart(Part):
    def __init__(self, millis) -> None:
        super().__init__()
        self.millis = millis

    def __call__(self, instance):
        millis = int(instance.var_or_val(self.millis))
        sleep(millis / 1000)

    def __str__(self) -> str:
        return ""

class Click(TimedPart):
    def __init__(self, millis, button, times) -> None:
        super().__init__(millis)
        self.button = button
        self.times = times

    def map_button(self, instance):
        MAP = [Button.left, Button.middle, Button.right]
        button = int(instance.var_or_val(self.button))
        if button <= 0 or button > 3:
            return Button.unknown
        else:
            return MAP[button - 1]

    def __call__(self, instance):
        super().__call__(instance)
        button = self.map_button(instance)
        times = int(instance.var_or_val(self.times))
        instance.controller.mouse_controller.click(button, times)

    def __str__(self) -> str:
        return f"{self.millis} click {self.button} {self.times}"

class Move(TimedPart):
    def __init__(self, millis, x, y, relative) -> None:
        super().__init__(millis)
        self.x = x
        self.y = y
        self.relative = relative

    def __call__(self, instance):
        super().__call__(instance)
        x = int(instance.var_or_val(self.x))
        y = int(instance.var_or_val(self.y))
        if instance.var_or_val(self.relative) == "true":
            instance.controller.mouse_controller.move(x, y)
        else:
            instance.controller.mouse_controller.position = (x, y)

    def __str__(self) -> str:
        return f"{self.millis} move {self.x} {self.y} {self.relative}"


class Key(TimedPart):
    def __init__(self, millis, key, is_down) -> None:
        super().__init__(millis)
        self.key = key
        self.is_down = is_down

    def __call__(self, instance):
        super().__call__(instance)
        key = instance.var_or_val(self.key)
        is_down = instance.var_or_val(self.is_down)
        is_down = is_down == "true" or is_down == "down" or is_down == "press"

        if hasattr(PynputKey, key):
            key = getattr(PynputKey, key)

        if is_down:
            instance.controller.keyboard_controller.press(key)
        else:
            instance.controller.keyboard_controller.release(key)

    def __str__(self) -> str:
        return f"{self.millis} key {self.key} {self.is_down}"


class Type(TimedPart):
    def __init__(self, millis, text) -> None:
        super().__init__(millis)
        self.text = text

    def __call__(self, instance):
        super().__call__(instance)
        text = instance.var_or_val(self.text)
        instance.controller.keyboard_controller.type(text)

    def __str__(self) -> str:
        return f"{self.millis} type {self.text}"

class Scroll(TimedPart):
    def __init__(self, millis, x, y) -> None:
        super().__init__(millis)
        self.x = x
        self.y = y

    def __call__(self, instance):
        super().__call__(instance)
        x = int(instance.var_or_val(self.x))
        y = int(instance.var_or_val(self.y))
        instance.controller.mouse_controller.scroll(x, y)

    def __str__(self) -> str:
        return f"{self.millis} scroll {self.x} {self.y}"


class Command(TimedPart):
    def __init__(self, millis, command) -> None:
        super().__init__(millis)
        self.command = command

    def __call__(self, instance):
        super().__call__(instance)
        command = instance.var_or_val(self.command)
        subprocess.run(command, shell=True)

    def __str__(self) -> str:
        return f"{self.millis} command {self.command}"
