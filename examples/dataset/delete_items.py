#!/usr/bin/env python3

#
# The following example shows how to delete an item from
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

# Deletion of an item requires to rebuild the sequential
# index. For large datasets this can be extremely slow when
# done for every deletion. The "with" statement below allows
# to postpone rebuilding the index for all the contained
# function calls.
# NOTE: while in the "with" scope the linear index becomes inconsisent
# and linear indices remain unchanged by the deletion.
# DO NOT ACCESS LINEAR INDICES OF DELETED ELEMENTS.
# NOTE: If you are only deleting a single item then the "with"
# statement is not required.
with ds.seq.deferred_index_rebuild():
    # Remove first group:
    #del ds.seq["scene_001"]

    # Remove first item in second group:
    # NOTE: this will delete the second group as well since it becomes
    # empty after deleting the item.
    #del ds.seq["scene_002"]["item_001"]

    # Delete the second item
    del ds[1]

# Save the modified dataset (will overwrite out_write_from_files)
ds.write()

print()
print("To view run: \"iviz out_write_from_files/data.json\"")
print()