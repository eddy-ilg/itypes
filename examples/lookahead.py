#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import lookahead

print()
sequence = [1, 2, 3, 4, 5]
print("sequence:", sequence)
print()

for item, has_next in lookahead(sequence):
    print('item:    ', item)
    print('nas_next:', has_next)
    print()