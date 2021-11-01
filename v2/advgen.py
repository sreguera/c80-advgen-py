# Copyright (C) 2021, Sebastián Reguera
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

engine_begin = """import random

class AdventureBase:

    def __init__(self):
        self.rooms = {}
        self.objects = {}
        self.verbs = {}
        self.obj_loc = {}
        self.conn = {}
        self.flags = {}
        self.you = 1

    def describe_room(self):
        print()
        print("You are %s" % self.rooms[self.you])
        print("You can see:")
        for (no, o) in self.objects.items():
            if self.obj_loc[no] == self.you:
                print(o, end=", ")
        print()
        print("You can go:")
        for d in self.dirs:
            if self.conn.get((self.you, d), 0) != 0:
                print(d, end=" "),
        print()

    def do_inv(self):
        for (no, o) in self.objects.items():
            if self.obj_loc[no] == -1:
                print(o)

    def do_score(self):
        t = 0
        y = 0
        for (no, o) in self.objects.items():
            if "*" in o:
                t += 1
                if self.obj_loc[no] == -1 or self.obj_loc[no] == self.you:
                    y += 1
        print("Out of %d points you have %d" % (t, y))

    def process_dir(self, phrase):
        word_to_dir = {
            "n": "north",
            "s": "south",
            "e": "east",
            "w": "west",
            "u": "up",
            "d": "down"
        }
        dir = word_to_dir.get(phrase, "none")
        new_you = self.conn.get((self.you, dir), 0)
        if new_you != 0:
            self.you = new_you
            return True
        else:
            return False

    def parse(self, phrase):
        verb = 0
        object = 0
        words = phrase.split()
        for (nw, w) in enumerate(words):
            words[nw] = w[:3]
        if len(words) >= 1:
            for (nv, v) in self.verbs.items():
                if v[:3] == words[0]:
                    verb = nv
        if len(words) >= 2:
            for (no, o) in self.objects.items():
                if o[:3] == words[1]:
                    object = no
        return (verb, object)

    def run(self):
        self.initialize()

        while True:
            self.describe_room()
            phrase = input("what now? ")
            if phrase[:3] == "inv":
                self.do_inv()
                continue
            elif phrase[:5] == "score":
                self.do_score()
                continue
            else:
                (verb, object) = self.parse(phrase)

            done = self.process_dir(phrase)
            if done:
                continue

            if self.one_word(phrase):
                object = 0

            done = self.process_verbs(verb, object)
            if not done:
                print("I don't understand.")

    def initialize(self):
        self.rooms[1] = "In an empty room."

    def one_word(self, phrase):
        return False
    
    def process_verbs(self, verb, object):
        return False
"""
engine_initialize = """
class Adventure(AdventureBase):

    def initialize(self):
        self.you = 1
"""
engine_one_word = """
    def one_word(self, phrase):
"""
engine_process_verbs = """
    def process_verbs(self, verb, object):
"""
engine_end = """

if __name__ == "__main__":
    Adventure().run()
"""

class AdvGen:

    def __init__(self):
        self.rooms = {}
        self.objects = {}
        self.verbs = {}
        self.flags = {}
        self.dirs = ["north", "south", "east", "west", "up", "down"]

    def run(self):
        self.output = open("program.py", "w")
        print(engine_begin, file=self.output)
        self.gen_initialize()
        self.gen_one_word()
        self.gen_process_verbs()
        print(engine_end, file=self.output)

    def gen_initialize(self):
        print(engine_initialize, file=self.output)

        # Room input
        self.rooms = read_rooms()
        for (nr, r) in self.rooms.items():
            print(f"        self.rooms[{nr}] = \"{r}\"", file=self.output)
        print()

        # Object input
        self.objects = read_objects()
        for (no, o) in self.objects.items():
            print(f"        self.objects[{no}] = \"{o}\"", file=self.output)
        print()

        # Verb input
        self.verbs = read_verbs()
        for (nv, v) in self.verbs.items():
            print(f"        self.verbs[{nv}] = \"{v}\"", file=self.output)
        print()

        # Object placement
        print()
        for (no, o) in self.objects.items():
            nr = choose_room(f"What room does the {o} go in? ", self.rooms)
            print(f"        self.obj_loc[{no}] = {nr}", file=self.output)    
        print()

        # Directions
        print("        self.dirs = [\"north\", \"south\", \"east\", \"west\", \"up\", \"down\"]", file=self.output)    

        # Direction chart
        conn = read_conns(self.rooms, self.dirs)
        for ((nr, d), nr2) in conn.items():
            print(f"        self.conn[({nr}, \"{d}\")] = {nr2}", file=self.output)
        print()

    def gen_one_word(self):
        print(engine_one_word, file=self.output)
        line = input("How many one word sentences? ")
        for i in range(int(line)):
            w = input("Word? ")
            print(f"        if phrase == \"{w}\":", file=self.output)
            print("            return True", file=self.output)
        print("        return False", file=self.output)

    def gen_process_verbs(self):
        print(engine_process_verbs, file=self.output)

        # verb object rules
        for (nv, v) in self.verbs.items():

            # Rules for this one verb
            while True:
                rule = ""
                print()
                print(f"The verb is {v}")

                # verb synonyms
                next = prompt("Do you want to use another verb (y/n)?", ["y", "n"])
                if next == "y":
                    nv1 = choose_verb("which one? ", self.verbs)
                    rule += f"        if verb == {nv}:\n"
                    rule += f"            return self.process_verbs({nv1}, self.object)"
                    print(rule, file=self.output)
                    break

                # Choose object for verb
                no = choose_object("Object number> ", self.objects)
                rule += f"        if verb == {nv} and object == {no}"

                # Add conditions to rule
                while True:
                    print_rule(rule)
                    next = prompt("Add more conditions (y/n)?", ["y", "n"])
                    if next == "n":
                        break
                    rule += self.read_condition()
                rule += ":\n"

                print_rule(rule)

                # Add actions to rule
                while True:
                    action = self.read_action()
                    rule += "            " + action + "\n"
                    print_rule(rule)
                    next = prompt("Add more actions (y/n)?", ["y", "n"])
                    if next == "n":
                        rule += "            return True"        
                        break
                
                print(rule, file=self.output)

                next = prompt("Add more rules for this verb (y/n)?", ["y", "n"])
                if next == "n":
                    break
        print("        return False", file=self.output)

    def read_condition(self):
        next = prompt("Do you want to add on 'and' or 'or' (a/o)?", ["a", "o"])
        if next == "a":
            cond = " and "
        else:
            cond = " or "
        opt = choose_from_menu({
            "1": "If object in room",
            "2": "If object in room or in inv",
            "3": "If flag is set",
            "4": "For random factor",
            "5": "If object not in room",
            "6": "If room = N"
        }, "to add what?")
        if opt == "1":
            on = choose_object("Which object? ", self.objects)
            cond += f"(self.obj_loc[{on}] == self.you)"
        elif opt == "2":
            on = choose_object("Which object? ", self.objects)
            cond += f"(self.obj_loc[{on}] == self.you or self.obj_loc[{on}] == -1)"
        elif opt == "3":
            f = choose_flag(self.flags)
            cond += f"(self.flags.get({f}, 0) != 0)"
        elif opt == "4":
            line = input("How many out of 100 are bad? ")
            cond += f"(random.randint(1, 100) > {int(line)})"
        elif opt == "5":
            on = choose_object("Which object? ", self.objects)
            cond += f"(self.obj_loc[{on}] != self.you)"
        elif opt == "6":
            nr = choose_room("What room?", self.rooms)
            cond += f"(self.you == {nr})"
        return cond

    def read_action(self):
        opt = choose_from_menu({
            "0": "Anything not in list",
            "1": "Object disappears",
            "2": "Object to inv",
            "3": "Leave object in room",
            "4": "Set flag",
            "5": "Reset flag",
            "6": "New object to room",
            "7": "Print",
            "8": "To open or close a passage"
        }, "to end with? ")
        if opt == "0":
            line = input("Other than string input: ")
            action = line
        elif opt == "1":
            on = choose_object("Which object? ", self.objects)
            action = f"self.obj_loc[{on}] = 0"
        elif opt == "2":
            on = choose_object("Which object? ", self.objects)
            action = f"self.obj_loc[{on}] = -1"
        elif opt == "3":
            on = choose_object("Which object? ", self.objects)
            action = f"self.obj_loc[{on}] = self.you"
        elif opt == "4":
            f = choose_flag(self.flags)
            action = f"self.flag[{f}] = 1"
        elif opt == "5":
            f = choose_flag(self.flags)
            action = f"self.flag[{f}] = 0"
        elif opt == "6":
            on = choose_object("Which object? ", self.objects)
            action = f"self.obj_loc[{on}] = self.you"
        elif opt == "7":
            line = input("To print what? ")
            action = f"print(\"{line}\")"
        elif opt == "8":
            r1 = choose_room("From which room?", self.rooms)
            r2 = choose_room("To which room?", self.rooms)
            dn = choose_dir("in which direction? ", self.dirs)
            action = f"self.conn[({r1}, \"{self.dirs[dn]}\")] = {r2}"
        return action

def print_rule(rule):
    print("")
    print("This is what you have so far:")
    print(rule)
    print("")

# Functions for managing tables in a generic way

def read_table(thing):
    print(f"Enter {thing}s. To end input cycle type .")
    things = {}
    nr = 1
    while True:
        line = input(f"{thing} number {nr}> ")
        if line == ".":
            break
        things[nr] = line
        nr += 1
    return things

def print_table(table):
    for (n, t) in table.items():
        print(f"{n} {t}")

def choose_from_table(table, prompt):
    while True:
        line = input(prompt + " [l to list items] ")
        if line == "l":
            print_table(table)
        else:
            return int(line)

# Functions for rooms

def read_rooms():
    return read_table("room")

def print_rooms(rooms):
    print_table(rooms)

def choose_room(prompt, rooms):
    return choose_from_table(rooms, prompt)

# Functions for objects

def read_objects():
    return read_table("object")

def print_objects(objects):
    print_table(objects)

def choose_object(prompt, objects):
    return choose_from_table(objects, prompt)

# Functions for verbs

def read_verbs():
    return read_table("verb")

def print_verbs(verbs):
    print_table(verbs)

def choose_verb(prompt, objects):
    return choose_from_table(objects, prompt)

# Functions for directions

def print_dirs(dirs):
    for (nd, d) in enumerate(dirs):
        print(f"{nd} {d}")

def choose_dir(prompt, dirs):
    while True:
        line = input(prompt + " [l to list dirs] ")
        if line == "l":
            print_dirs(dirs)
        else:
            return int(line)

# Functions for connections

def read_conns(rooms, dirs):
    conn = {}
    for (nr, r) in rooms.items():
        for d in dirs:
            if d == "up" or d == "down":
                q = f"Where does the room '{r}' lead {d}? "
            else:
                q = f"Where does the room '{r}' lead to in the {d}? "
            nr2 = choose_room(q, rooms)
            conn[(nr, d)] = nr2
    return conn

# Functions for flags

def print_flags(flags):
    for (nf, f) in flags.items():
        print(f"{nf} {f}")

def choose_flag(flags):
    print_flags(flags)
    next = prompt("Some of these flags (y/n)?", ["y", "n"])
    if next == "y":
        line = input("Which one? ")
        f = int(line)
    if next == "n":
        if flags.keys():
            last_flag = max(flags.keys()) + 1
        else:
            last_flag = 1
        line = input("What is for? ")
        flags[last_flag] = line
        f = last_flag
    return f

# Utilities

def prompt(text, options):
    s = ""
    while s not in options:
        s = input(text + " ")
    return s

def choose_from_menu(menu, prompt_str):
    for k, v in menu.items():
        print(f"{k} {v}")
    return prompt(prompt_str, menu.keys())

if __name__ == "__main__":
    AdvGen().run()

