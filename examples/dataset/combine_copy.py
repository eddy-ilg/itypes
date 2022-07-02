#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#!/usr/bin/env python3

#
# The following example shows how to create a new sequence as a
# combination of two sequences by copying their data.
#

#
# Generate sequences
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
# Note that  contents of "out_write_from_files" are:
# (linear_index, group_id, item_id)
# (0, scene_001, item_001)
# (1, scene_001, item_002)
# (2, scene_002, item_001)

print()
print("Running: \"python3 ./write_from_tensors.py > /dev/null\"")
os.system("python3 ./write_from_tensors.py > /dev/null")
# Note that  contents of "out_write_from_files" are:
# (linear_index, group_id, item_id)
# (0, scene1, 0000)
# (1, scene1, 0001)
# (2, scene2, 0000)

# You can use "ds print <folder_name>" to see the contents above

#
# Access sequences
#
from itypes import Dataset
ds1 = Dataset("out_write_from_files").read()
ds2 = Dataset("out_write_from_tensors").read()

#
# Create a combined sequence
#
ds = Dataset("out_combine_copy/data.json", auto_write=True)

# Copy the visualizations
# (this creates empty variables)
ds.viz.copy_from(ds2.viz)

# Delete the occ variable and visualization
del ds.var["occ"]

# You could also copy single visualizations instead:
# ds.viz["image0"] = ds2.viz["image0"]
# ds.viz["image1"] = ds2.viz["image1"]
# ds.viz["flow"] = ds2.viz["flow"]

# Copy the sequence structure
ds.seq.copy_from(ds2.seq)

# Copy the data from ds2
# (by referencing the files)
# Note that values will be looked up by their group_id and item_id
ds.var["image0"].copy_from(ds2.var["image0"], mode="copy", indexing="id")
ds.var["image1"].copy_from(ds2.var["image0"], mode="copy", indexing="id")

# Copy the data from ds1
# (by referencing the files)
# Note that the names in ds1 are different and we need to use a linear index
# to find the right ones. Values in ds1 will be looked up by using linear
# indices of the dataset.
ds.var["flow"].copy_from(ds1.var["flow"], mode="copy", indexing="linear")

# You could also copy all from ds2 by using:
#ds.var.copy_from(ds2.var, mode="copy")

print()
print("Created dataset:")
print(ds.str(prefix="  "))
print()