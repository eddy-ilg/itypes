#!/usr/bin/env python3

#
# Configure logging
#
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Show debugging output.")
args = parser.parse_args()
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level, format='[%(levelname)8s] %(name)-15s : %(message)s')

#
# The following demonstrates random access
# operations on sequences.
#

#
# Generate a sequence
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
from itypes import Sequence

seq = Sequence("out_write_from_files/data.gridseq").read()

device = "numpy"

# Access by linear index
frame = seq.frames()[0]
# NOTE that you can also access single ids as in read_linear_entry.py
struct = frame.torch_struct("hwc", device)
print('Read frame:')
print(struct)
print()

# Access by scene and frame name
frame = seq.data["Scene-001"]["0000000001"]
# NOTE that you can also access single ids as in read_linear_entry.py
struct = frame.torch_struct("hwc", device)
print('Read frame:')
print(struct)
print()
