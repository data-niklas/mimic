#!/usr/bin/env python3
from pynput.keyboard import Key

def parse_key(key):
    key_string = str(key)
    return key_string.replace("Key.", "").replace("'","")


def parse_button(button):
    button_string = str(button)
    return button_string.replace("Button.", "").replace("left", "1")


def str_to_key(text):
    if hasattr(Key, text):
        return getattr(Key, text)
    return text
