#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import Struct
from itypes import is_number, is_list

print()


# From dictionary
x = {
    'a': 1,
    'b': {
        'c': 2,
        'd': 3
    }
}
s = Struct(x)
print("s:")
print(s)
print()

# A nested struct
s = Struct()
s.member1 = "a str"
s.member2 = 3
s.member3 = Struct()
s.member3.a = [1, 2, 3]
s.member3.b = 5

print("s:")
print(s)
print()


# Translate example
def mul_by_two(x):
    if is_number(x):
        x = 2*x
    return x

# NOTE: s is unchanged
s2 = s.translate(mul_by_two)

print("translate result:")
print(s2)
print()


# Apply example
def insert_six(x):
    if is_list(x):
        x.insert(6)
    return x

s.apply(insert_six)

print("s after apply:")
print(s)
print()


# Flatten keys example
# NOTE: s is unchanged
k = s.flat_keys()
print('flat_keys result:')
print(k)
print()



# Flatten exammple
# NOTE: s is unchanged
f = s.flatten()
print('flatten result:')
print(f)
print()

# Merge exammple
a = Struct()
a.member1 = "a str"
a.member2 = 3
a.member3 = Struct()
a.member3.a = [1, 2, 3]
print("sturct a:")
print(a, end='')

b = Struct()
b.member3 = Struct()
b.member3.b = 16
b.member4 = 27
print("sturct b:")
print(b, end='')
m = a.merge_with(b)
print("merged:")
print(m, end='')
print("sturct a:")
print(a, end='')
print("sturct b:")
print(b, end='')
print()



