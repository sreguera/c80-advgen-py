# The Adventure Generator

A reimplementation in Python of "The Adventure Generator", by David Huntress, published in 1981 in "The Captain 80 Book of BASIC Adventures".

## V1 - Direct conversion

The v1 directory contains a more or less direct translation of the original BASIC program into python.
* One single file corresponding to the BASIC program.
* No functions. The original BASIC program did not use GOSUB.
* No libraries. Only the minimum from the Python standard library for e.g. RNG.

The only simplifications with respect to the original BASIC program are:
* up and down are treated in the same way as the other directions.
* flags can be created in the conditions section, not only in the actions section.

To execute the program just type:
```
python advgen.py
```
The file test_adv.txt contain the
```
cat test_adv.txt | python uncomment.py | python advgen.py
```