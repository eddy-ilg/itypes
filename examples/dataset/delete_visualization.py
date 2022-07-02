#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how to delete a visualization from
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

# Delete the occlusion visualization
# NOTE: this will not delete the variable. To remove both, the variable
# and the visualization delete the variable (see delete_variable.py)
del ds.viz["occ"]

# Save the modified dataset (will overwrite out_write_from_files)
ds.write()

print()
print("To view run: \"iviz out_write_from_files/data.json\"")
print()