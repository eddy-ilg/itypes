#!/usr/bin/env python3

#
# The following demonstrates random access
# operations on datasets.
#

#
# Generate a dataset
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()
print()

#
# Read single items in linear mode
#
import itypes
from itypes import Dataset

ds = Dataset("out_write_from_files/data.json").read()

device = "numpy"

# Access by linear index
item = ds[0]
# NOTE that you can also access single ids as in read_linear_entry.py
struct = item.torch_struct("hwc", device)
print('Read frame:')
print(struct)
print()

# Access by scene and frame name
item = ds.seq["scene_001"]["item_001"]
# NOTE that you can also access single ids as in read_linear_entry.py
struct = item.torch_struct("hwc", device)
print('Read frame:')
print(struct)
print()
