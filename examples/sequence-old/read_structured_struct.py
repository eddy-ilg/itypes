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
# The following example shows how to read and structurally
# iterate through a sequence, reading frames as structs.
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
from itypes import Sequence

seq = Sequence("out_write_from_files/data.gridseq").read()

device = "numpy"

print()
for scene in seq.data:
    for frame in scene:
        # NOTE: for reading structs everything is float32 by default
        struct = frame.torch_struct("hwc", device)

        print('Read frame:')
        print(struct)
        print()