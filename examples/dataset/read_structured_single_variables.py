#!/usr/bin/env python3

#
# The following example shows how to read and linearly
# iterate through a dataset, reading single tensors.
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
from itypes import Dataset

ds = Dataset("out_write_from_files/data.json").read()

print(f'Datatset length: {len(ds)}')
print()

for group in ds.seq:
    for item in group:
        image0 = item['image0'].data(dims="hwc", device="numpy", dtype=itypes.float32)
        image1 = item['image1'].data(dims="hwc", device="numpy", dtype=itypes.float32)
        flow = item['flow'].data(dims="hwc", device="numpy", dtype=itypes.float32)
        occ = item['occ'].data(dims="hwc", device="numpy", dtype=itypes.bool)

        def print_info(id, data):
            print(f'  {id:10} type={type(data)}, shape={data.shape}, dtype={data.dtype}')

        print('Read frame:')
        print_info("image0", image0)
        print_info("image1", image1)
        print_info("flow", flow)
        print_info("occ", occ)
        print()