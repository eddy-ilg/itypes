#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how to read and linearly
# iterate through a dataset, reading items as structs.
#

#
# Generate a sequence
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()

#
# Read single items in linear mode
#
from itypes import Dataset

ds = Dataset("out_write_from_files/data.json").read()

device = "numpy"

print()
for group in ds.seq:
    for item in group:
        # NOTE: for reading structs everything is float32 by default
        struct = item.torch_struct("hwc", device)

        print('Read item:')
        print(struct)
        print()