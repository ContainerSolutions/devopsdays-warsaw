#!/usr/bin/env nix-shell
#!nix-shell -i python3 -p python3 python3Packages.pyyaml python3Packages.ansicolors xdotool

# NOTE! also adjust keep_floating.
dev = "SEM Trust Numpad"
#dev = "HID 04d9:a02a" # microtools numpad
#dev = "Dell Dell USB Keyboard"

import subprocess
import re
import yaml
import colors
import os

NUM_MIN=82
NUM_PLUS=86
NUM_ENTER=104
NUM_STAR=63
NUM_BACKSPACE=22
NUM_DIV=106
NUM_END=87
NUM_PAGE_DOWN=89
NUM_PAGE_UP=81
NUM_TAB=23

NUM_UP=80
NUM_DOWN=88

NUM_HOME=79

KEYMAPPING={
        "&": "ampersand",
        "'": "apostrophe",
        "~": "asciitilde",
        "\\": "backslash",
        "|": "bar",
        ":": "colon",
        ",": "comma",
        "=": "equal",
        "-": "minus",
        "\n": "Return",
        ".": "period",
        '"': "quotedbl",
        ";": "semicolon",
        "/": "slash",
        ' ': "space",
        '$': "dollar",
        '>': "greater",
        '_': "underscore",
        '(': "parenleft",
        ')': "parenright",
        '{': "braceleft",
        '}': "braceright",
        '[': "bracketleft",
        ']': "bracketright",
        '#': "numbersign",
        '!': "exclam",
        }

for l in "abcdefghijklmnopqrstuvwxyz1234567890":
    KEYMAPPING[l] = l
    u = l.upper()
    KEYMAPPING[u] = u

def get_dev_id(dev):
    list_process = subprocess.Popen(["xinput", "list"], stdout=subprocess.PIPE)
    lines = list_process.stdout.read().decode("utf-8").split("\n")

    for line in lines:
        parts = line.split("\t")
        if dev in parts[0] and "floating" in parts[2]:
            return parts[1].split("=")[1]

    return None

def get_numpad_characters(dev):
    proc = subprocess.Popen(['xinput','test', get_dev_id(dev)],stdout=subprocess.PIPE)
    regex = re.compile("^key release (\d+)$")
    for line in iter(proc.stdout.readline,''):
        line = line.decode("utf-8").strip()
        result = regex.match(line)
        if result:
            code = int(result[1])
            yield code

class Livecoding:
    def __init__(self, script):
        self.position = 0
        self.repeat = False
        self.steps = script["steps"]
        self.swap_between_one_and_two = True

    def on_char(self, char):
        # SWITCHING MODES
        if char == NUM_TAB:
            if self.swap_between_one_and_two:
                Livecoding.xdotool("key", "Super_L+1")
            else:
                Livecoding.xdotool("key", "Super_L+2")

            self.swap_between_one_and_two = not self.swap_between_one_and_two

        # LIVECODING

        # enter
        if char == NUM_ENTER:
            self.enter_step(self.position)
            if not self.repeat:
                self.position += 1
        if char == NUM_STAR:
            self.repeat = not self.repeat

        # position
        if char == NUM_PLUS:
            self.position += 1
        if char == NUM_MIN:
            self.position -= 1
        #if char == NUM_END:
        #    self.position = len(self.steps) - 1

        if char == NUM_UP:
            Livecoding.xdotool("key", "Shift+Prior")
        if char == NUM_DOWN:
            Livecoding.xdotool("key", "Shift+Next")

        if char == NUM_BACKSPACE:
            Livecoding.xdotool("key", "Control+C")

        # SLIDES
        if char == NUM_PAGE_UP:
            Livecoding.xdotool("key", "Prior")
        if char == NUM_PAGE_DOWN:
            Livecoding.xdotool("key", "Next")

        # Sanity checking
        if self.position > (len(self.steps)-1):
            self.position = len(self.steps) - 1
        if self.position < 0:
            self.position = 0

    def print_state(self):
        subprocess.call(["tput", "reset"])

        step = self.steps[self.position]["cmd"]

        if self.position > 0:
            prevStep = self.steps[self.position-1]["cmd"]
        else:
            prevStep = "-"

        if self.position < len(self.steps) -1:
            nextStep = self.steps[self.position+1]["cmd"]
        else:
            nextStep = "-"

        if self.repeat:
            print(colors.color("*** REPEATING ***", fg="red", style="bold"))

        print("prev   ", colors.color(prevStep.replace("\n", "\n        "), style="crossed"))
        print()
        print("current", colors.color(step.replace("\n", "\n        "),style="bold"))
        print()
        print("next   ", colors.color(nextStep.replace("\n", "\n        "), style="italic"))

        print()
        print("+ => next, - => prev, * => repeat, <Enter> => enter && +, <End> => Jump to last")
        print("backspace => <CTRL+C>, <PageUp> => <Shift+PageUp>, <PageDown> => <Shift+PageDown>")

    def enter_step(self, position):
        step = self.steps[position]

        if "cmd" in step:
            cmd = step["cmd"] + "\n"
            mapped = [KEYMAPPING[c] for c in cmd]
            Livecoding.xdotool("key", * mapped)
        else:
            raise "unknown command"

    def xdotool(*args):
        subprocess.call(["xdotool", *args])

if __name__ == "__main__":
   subprocess.call(["xinput", "float", dev])

   print("Starting keyboard playback")

   script = yaml.load(open("livecoding.yaml", 'r'))

   # Filter all skipped steps
   script["steps"] = [x for x in script["steps"] if not x.get("skip", False)]

   livecoding = Livecoding(script)

   livecoding.print_state()

   for char in get_numpad_characters(dev):
        livecoding.on_char(char)
        livecoding.print_state()
        print("pressed", char)
