#!/usr/bin/env python3

#
# The following example shows how to create a dataset using
# another one as a template.
#

#
# Generate sequence
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()

#
# Create sequence
#
from itypes import Dataset

# Create sequence
ds = Dataset(file='out_metrics/data.json', auto_write=True)

# Copy the dataset
ds.copy_from(Dataset("out_write_from_files/data.json").read(), mode="copy")

# Create a metric
met = ds.met.create(type="EPE", id="EPE", data="flow", ref="flow", crop_boundary=4)

value = met.compute(save_values=False, save_maps=False, save_result=False)
print("Computed metric:", value)
print()

# Test update (recomputes only missing values)
value = met.update(save_values=True, save_maps=True)

print("Dataset:")
print(ds)

# Test dataset copy
ds_copy = Dataset()
ds_copy.copy_from(ds)
print("Copied dataset:")
print(ds_copy)


print("To view run: \"iviz out_metrics/data.json\"")
print()
