#!/usr/bin/env python3

from z3 import *

# Key has three numbers, call them k1, k2, k3
k1, k2, k3 = Ints('k1 k2 k3')

s = Solver()

# Key numbers are in the range 0-9
s.add([k >= 0 for k in [k1, k2, k3]])
s.add([k <= 9 for k in [k1, k2, k3]])

# a or b or c is in the correct position while
# the other two are not in the key at all
def one_right_rightplace(a, b, c):
    s.add(Or(
        # a correct in right place
        And(k1 == a, k2 != a, k2 != b, k2 != c, k3 != a, k3 != b, k3 != c),
        # b correct in right place
        And(k1 != a, k1 != b, k1 != c, k2 == b, k3 != a, k3 != b, k3 != c),
        # c correct in right place
        And(k1 != a, k1 != b, k1 != c, k2 != a, k2 != b, k2 != c, k3 == c)
    ))

# One correct digit is in the wrong position
# The other two digits are not in the key
def one_right_wrongplace(a, b, c):
    # Nobody in correct place
    s.add(k1 != a, k2 != b, k3 != c)
    s.add(Or(
        # a correct in wrong place
        And(k2 == a, k1 != b, k1 != c, k3 != a, k3 != b),
        And(k3 == a, k1 != b, k1 != c, k2 != a, k2 != c),
        # b correct in wrong place
        And(k1 == b, k2 != a, k2 != c, k3 != a, k3 != b),
        And(k3 == b, k1 != b, k1 != c, k2 != a, k1 != c),
        # c correct in wrong place
        And(k1 == c, k2 != a, k2 != c, k3 != a, k3 != b),
        And(k2 == c, k1 != b, k1 != c, k3 != a, k3 != b)
        ))

# Two correct digit are in the wrong position
# The third digit is not in the key
def two_right_wrongplace(a, b, c):
    # Nobody in correct place
    s.add(k1 != a, k2 != b, k3 != c)
    s.add(Or(
        # a, b correct in wrong place
        # * a b
        And(k1 != b, k1 != c, k2 == a, k3 == b),
        # b * a
        And(k1 == b, k2 != a, k2 != c, k3 == a),
        # b a *
        And(k1 == b, k2 == a, k3 != a, k3 != b),
        # a, c correct in wrong place
        # * c a
        And(k1 != b, k1 != c, k2 == c, k3 == a),
        # c * a
        And(k1 == c, k2 != a, k2 != c, k3 == c),
        # c a *
        And(k1 == c, k2 == a, k3 != a, k3 != b),
        # b, c correct in wrong place
        # * c b
        And(k1 != b, k1 != c, k2 == c, k3 == b),
        # c * b
        And(k1 == c, k2 != a, k2 != c, k3 == b),
        # b c *
        And(k1 == b, k2 == c, k3 != a, k3 != b)
        ))

# All digits are incorrect (not in key)
def all_wrong(a, b, c):
    s.add(k1 != a, k1 != b, k1 != c)
    s.add(k2 != a, k2 != b, k2 != c)
    s.add(k3 != a, k3 != b, k3 != c)

# Here comes the puzzle from the milk packet
one_right_rightplace(6, 8, 2)
one_right_wrongplace(6, 1, 4)
two_right_wrongplace(2, 0, 6)
# The 3 constraints above are enough to solve it
# the constraints below are superfluous
all_wrong(7, 3, 8)
one_right_wrongplace(8, 7, 0)

res = s.check()
if res == sat:
    # print one solution (many might exist)
    m = s.model()
    print(m[k1], m[k2], m[k3])
else:
    # unsat means no solution found
    print(res)

