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
# The following example shows how to read and linearly
# iterate through a sequence, reqding single tensors.
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
import itypes
from itypes import Sequence

seq = Sequence("out_write_from_files/data.gridseq").read()

print()
for frame in seq.frames():
    image0 = frame.data('image0', dims="hwc", device="numpy", dtype=itypes.float32)
    image1 = frame.data('image1', dims="hwc", device="numpy", dtype=itypes.float32)
    flow = frame.data('flow', dims="hwc", device="numpy", dtype=itypes.float32)
    occ = frame.data('occ', dims="hwc", device="numpy", dtype=itypes.bool)

    def print_info(id, data):
        print(f'  {id:10} type={type(data)}, shape={data.shape}, dtype={data.dtype}')

    print('Read frame:')
    print_info("image0", image0)
    print_info("image1", image1)
    print_info("flow", flow)
    print_info("occ", occ)
    print()