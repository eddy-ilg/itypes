#!/usr/bin/env python3

#
# The following example shows how to conveniently fill in a single item sequence directly.
#
from itypes import Dataset

# Create dataset with a single item
ds = Dataset(file='out_write_single_item_from_files/data.json', single_item=True, auto_write=True)

# First row: show images
with ds.viz.new_row() as row:
    row.add_cell('image', var='image0').sv.set_ref('../data/scene1/0000-image0.png')
    row.add_cell('image', var='image1').sv.set_ref('../data/scene1/0000-image1.png')
    row.add_cell('flow',  var='flow').sv.set_ref('../data/scene1/0000-flow.flo')

# Second row: show flow and occlusions
with ds.viz.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', var='occ').sv.set_ref('../data/scene1/0000-occ.png')

print()
print("To view run: \"iviz out_write_single_item_from_files/data.json\"")
print()










