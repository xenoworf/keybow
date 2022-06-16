from pmk import PMK
from pmk.platform.keybow2040 import Keybow2040 as Hardware

import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.keyboard_layout_us import KeyboardLayoutUS
from adafruit_hid.keycode import Keycode

# Set up Keybow
keybow = PMK(Hardware())
keys = keybow.keys

# Set up the keyboard and layout
keyboard = Keyboard(usb_hid.devices)
layout = KeyboardLayoutUS(keyboard)

# A map of keycodes that will be mapped sequentially to each of the keys, 0-15
keymap = [
    ["f9"],
    ["delete"],
    ["control", "y"],
    ["control", "z"],  # 0x0-3
    ["left", "f11"],
    ["grave"],
    ["left"],
    ["tab"],  # 0x4-7
    ["shift", "f12"],
    ["insert"],
    ["down"],
    ["up"],  # 0x8-B
    [],
    ["backspace"],
    ["right"],
    ["space"],  # 0xC-F
]

keycodes = {
    "backspace": Keycode.BACKSPACE,
    "control": Keycode.LEFT_CONTROL,
    "delete": Keycode.DELETE,
    "down": Keycode.DOWN_ARROW,
    "f11": Keycode.F11,
    "f12": Keycode.F12,
    "f9": Keycode.F9,
    "grave": Keycode.GRAVE_ACCENT,
    "insert": Keycode.INSERT,
    "left": Keycode.LEFT_ARROW,
    "right": Keycode.RIGHT_ARROW,
    "shift": Keycode.LEFT_SHIFT,
    "space": Keycode.SPACEBAR,
    "tab": Keycode.TAB,
    "up": Keycode.UP_ARROW,
    "y": Keycode.Y,
    "z": Keycode.Z,
}


colors = {
    "red": (255, 0, 0),
    "off": (0, 0, 0),
    "yellow": (255, 255 // 2, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
}

rgb_map = [
    "red",
    "off",
    "yellow",
    "yellow",  # 0-3
    "off",
    "green",
    "blue",
    "off",  # 4-7
    "off",
    "green",
    "blue",
    "blue",  # 8-B
    "red",
    "off",
    "blue",
    "off",  # C-F
]

for key in keys:
    color = rgb_map[key.number]
    key.set_led(*colors[color])

    @keybow.on_press(key)
    def press_handler(key):
        mapping = keymap[key.number]
        codes = [keycodes[c] for c in mapping]
        print(f"Press {mapping} {codes}")
        keyboard.send(*codes)

    @keybow.on_release(key)
    def release_handler(key):
        mapping = keymap[key.number]
        print(f"Release {mapping}")

    @keybow.on_hold(key)
    def hold_handler(key):
        mapping = keymap[key.number]
        print(f"Hold {mapping}")

while True:
    keybow.update()
