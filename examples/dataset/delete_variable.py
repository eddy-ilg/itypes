#!/usr/bin/env python3

#
# The following example shows how to delete a variable from
# a dataset.
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

# Delete the occ variable
# NOTE: This will automatically also delete all visualizations
# that reference the pcc variable.
del ds.var["occ"]

# Save the modified dataset (will overwrite out_write_from_files)
ds.write()

print()
print("To view run: \"iviz out_write_from_files/data.json\"")
print()