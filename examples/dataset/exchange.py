#!/usr/bin/env python3

#!/usr/bin/env python3

#
# The following example shows how to exchange a variable from a sequence
# referencing the source files.
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
ds = Dataset("out_exchange/data.json", auto_write=True)
ds.copy_from(ds2, mode="ref")

# Exchange the flow variable to the one from ds2
ds.var["flow"].copy_from(ds1.var["flow"], mode="ref")


print()
print("Created dataset:")
print(ds.str(prefix="  "))
print()