import sys

for line in sys.stdin:
    line = line[:line.find("#")]
    if not line == "":
        print(line.strip())