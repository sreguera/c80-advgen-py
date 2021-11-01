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

output = open("program.py", "w")
rooms = {}
objects = {}
verbs = {}
flags = {}
last_flag = 0
print("import random", file=output)
print("rooms = {}", file=output)
print("objects = {}", file=output)
print("verbs = {}", file=output)
print("obj_loc = {}", file=output)
print("conn = {}", file=output)
print("flags = {}", file=output)

print("To end input cycle type .")
print()

# Room input
nr = 1
while True:
    line = input("Room number %d> " % nr)
    if line == ".":
        break
    rooms[nr] = line
    print("rooms[%d] = \"%s\"" % (nr, line), file=output)
    nr += 1
print()

# Object input
no = 1
while True:
    line = input("Object %d> " % no)
    if line == ".":
        break
    objects[no] = line
    print("objects[%d] = \"%s\"" % (no, line), file=output)
    no += 1
print()

# Verb input
nv = 1
while True:
    line = input("Verb %d> " % nv)
    if line == ".":
        break
    verbs[nv] = line
    print("verbs[%d] = \"%s\"" % (nv, line), file=output)
    nv += 1
print()

# Object placement
for (nr, r) in rooms.items():
    print("%d %s" % (nr, r))
print()
for (no, o) in objects.items():
    line = input("What room does the %s go in? " % o)
    print("obj_loc[%d] = %d" % (no, int(line)), file=output)    
print()

# Directions
dirs = ["north", "south", "east", "west", "up", "down"]
print("dirs = [\"north\", \"south\", \"east\", \"west\", \"up\", \"down\"]", file=output)    

# Direction chart
for (nr, r) in rooms.items():
    for (nr1, r1) in rooms.items():
        print("%d %s" % (nr1, r1))
    print()
    for d in dirs:
        if d == "up" or d == "down":
            q = "Where does the room \"%s\" lead %s? " % (r, d)
        else:
            q = "Where does the room \"%s\" lead to in the %s? " % (r, d)
        line = input(q)
        print("conn[(%d, \"%s\")] = %d" % (nr, d, int(line)), file=output)    
    print()

engine = """you = 1
while True:
    print()
    print("You are %s" % rooms[you])
    print("You can see:")
    for (no, o) in objects.items():
        if obj_loc[no] == you:
            print(o, end=", ")
    print()
    print("You can go:")
    for d in dirs:
        if conn[(you, d)] != 0:
            print(d, end=" "),
    print()
    phrase = input("what now? ")
    if phrase[:3] == "inv":
        for (no, o) in objects.items():
            if obj_loc[no] == -1:
                print(o)
    elif phrase[:5] == "score":
        t = 0
        y = 0
        for (no, o) in objects.items():
            if "*" in o:
                t += 1
                if obj_loc[no] == -1 or obj_loc[no] == you:
                    y += 1
        print("Out of %d points you have %d" % (t, y))
    else:
        verb = 0
        object = 0
        words = phrase.split()
        for (nw, w) in enumerate(words):
            words[nw] = w[:3]
        if len(words) >= 1:
            for (nv, v) in verbs.items():
                if v[:3] == words[0]:
                    verb = nv
        if len(words) >= 2:
            for (no, o) in objects.items():
                if o[:3] == words[1]:
                    object = no
"""
print(engine, file=output)

line = input("How many one word sentences? ")
for i in range(int(line)):
    w = input("Word? ")
    print("        if phrase == \"%s\":" % w, file=output)
    print("            object = 0", file=output)

engine2 = """
        done = True
        if phrase == "n" and conn[(you, "north")] != 0:
            you = conn[(you, "north")]
        elif phrase == "s" and conn[(you, "south")] != 0:
            you = conn[(you, "south")]
        elif phrase == "e" and conn[(you, "east")] != 0:
            you = conn[(you, "east")]
        elif phrase == "w" and conn[(you, "west")] != 0:
            you = conn[(you, "west")]
        elif phrase == "u" and conn[(you, "up")] != 0:
            you = conn[(you, "up")]
        elif phrase == "d" and conn[(you, "down")] != 0:
            you = conn[(you, "down")]
        else:
            done = False
"""
print(engine2, file=output)

# verb object rules
for (nv, v) in verbs.items():

    # Rules for this one verb
    while True:
        rule = ""
        for (no, o) in objects.items():
            print("%d %s" % (no, o))
        print()
        print("The verb is %s" % v)
        rule = "        if verb == %d" % nv

        # verb synonyms
        next = ""
        while next not in ["y", "n"]:
            next = input("Do you want to use another verb (y/n)? ")
        if next == "y":
            for (nv1, v1) in verbs.items():
                print("%d %s" % (nv1, v1))
            line = input("which one? ")
            rule += ":\n"
            rule += "            verb = %d" % int(line)
            print(rule, file=output)
            break

        # Choose object for verb
        line = input("Object number> ")
        rule += " and object == %d" % int(line)

        # Add conditions to rule
        while True:
            print("This is what you have so far:")
            print(rule)
            next = ""
            while next not in ["y", "n"]:
                next = input("Add more conditions (y/n)? ")
            if next == "n":
                break

            while next not in ["a", "o"]:
                next = input("Do you want to add on 'and' or 'or' (a/o)? ")
            if next == "a":
                rule += " and "
            else:
                rule += " or "
            print("1 If object in room")
            print("2 If object in room or in inv")
            print("3 If flag is set")
            print("4 For random factor")
            print("5 If object not in room")
            print("6 If room = N")
            opt = input("to add what? ")
            if opt == "1":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "(obj_loc[%d] == you)" % int(line)
            elif opt == "2":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "(obj_loc[%d] == you or obj_loc[%d] == -1)" % (int(line), int(line))
            elif opt == "3":
                for (nf, f) in flags.items():
                    print("%d %s" % (nf, f))
                next = ""
                while next not in ["y", "n"]:
                    next = input("Some of these flags (y/n)? ")
                if next == "y":
                    line = input("Which one? ")
                    f = int(line)
                if next == "n":
                    line = input("What is for? ")
                    last_flag += 1
                    flags[last_flag] = line
                    f = last_flag
                rule += "(flags.get(%d, 0) != 0)" % f
            elif opt == "4":
                line = input("How many out of 100 are bad? ")
                rule += "(random.randint(1, 100) > %d)" % int(line)
            elif opt == "5":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "(obj_loc[%d] != you)" % int(line)
            elif opt == "6":
                for (nr, r) in rooms.items():
                    print("%d %s" % (nr, r))
                line = input("What room? ")
                rule += "(you == %d)" % int(line)

        rule += ":\n"

        # Add actions to rule
        while True:
            print("0 Anything not in list")
            print("1 Object disappears")
            print("2 Object to inv")
            print("3 Leave object in room")
            print("4 Set flag")
            print("5 Reset flag")
            print("6 New object to room")
            print("7 Print")
            print("8 To open or close a passage")
            print(rule)
            print("")
            opt = input("to end with? ")
            if opt == "0":
                line = input("Other than string input: ")
                rule += "            %s\n" % line
            elif opt == "1":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "            obj_loc[%d] = 0\n" % int(line)
            elif opt == "2":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "            obj_loc[%d] = -1\n" % int(line)
            elif opt == "3":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "            obj_loc[%d] = you\n" % int(line)
            elif opt == "4":
                for (nf, f) in flags.items():
                    print("%d %s" % (nf, f))
                next = ""
                while next not in ["y", "n"]:
                    next = input("Some of these flags (y/n)? ")
                if next == "y":
                    line = input("Which one? ")
                    f = int(line)
                if next == "n":
                    line = input("What is for? ")
                    last_flag += 1
                    flags[last_flag] = line
                    f = last_flag
                rule += "            flag[%d] = 1\n" % f
            elif opt == "5":
                for (nf, f) in flags.items():
                    print("%d %s" % (nf, f))
                next = ""
                while next not in ["y", "n"]:
                    next = input("Some of these flags (y/n)? ")
                if next == "y":
                    line = input("Which one? ")
                    f = int(line)
                if next == "n":
                    line = input("What is for? ")
                    last_flag += 1
                    flags[last_flag] = line
                    f = last_flag
                rule += "            flag[%d] = 0\n" % f
            elif opt == "6":
                for (no, o) in objects.items():
                    print("%d %s" % (no, o))
                line = input("Which object? ")
                rule += "            obj_loc[%d] = you\n" % int(line)
            elif opt == "7":
                line = input("To print what? ")
                rule += "            print(\"%s\")\n" % line
            elif opt == "8":
                for (nr, r) in rooms.items():
                    print("%d %s" % (nr, r))
                r1 = input("From which room? ")
                r2 = input("To which room? ")
                for (nd, d) in enumerate(dirs):
                    print("%d  %s" % (nd, d))
                dir = input("in which direction? ")
                rule += "            conn[(%d, \"%s\")] = %d\n" % (r1, dirs[int(dir)], r2)    
            print("")
            print("This is what you have so far:")
            print(rule)
            print("")
            next = ""
            while next not in ["y", "n"]:
                next = input("Add more actions (y/n)? ")
            if next == "n":
                rule += "            done = True"
                print(rule, file=output)
                break

        next = ""
        while next not in ["y", "n"]:
            next = input("Add more rules for this verb (y/n)? ")
        if next == "n":
            break
        
print("        if not done:", file=output)
print("            print(\"I don't understand.\")", file=output)


        

    

    


