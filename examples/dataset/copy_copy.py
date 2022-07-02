#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#!/usr/bin/env python3

#
# The following example shows how to copy a sequence
# by copying the source files.
#

#
# Generate sequences
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()

# You can use "ds print <folder_name>" to see the contents above

#
# Access sequences
#
from itypes import Dataset
ds_existing = Dataset("out_write_from_files").read()

#
# Create a new sequence
#
ds = Dataset("out_copy_copy/data.json", auto_write=True)

# Copy the entire dataset, copying the files to the output folder
ds.copy_from(ds_existing, mode="copy")

print()
print("Created dataset:")
print(ds.str(prefix="  "))
print()