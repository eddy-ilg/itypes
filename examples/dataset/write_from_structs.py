#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how to create a sequence from
# torch structs that are already in memory.
#

import torch
import itypes
from itypes import Dataset, TorchStruct

# Read data into memory structs
device = torch.device("cuda")  # Note: this could be "numpy" as well

scene1_frame1 = TorchStruct(dims = "bchw", device=device)
scene1_frame1.read('image0', '../data/scene1/0000-image0.png', dtype=itypes.float32)
scene1_frame1.read('image1', '../data/scene1/0000-image1.png', dtype=itypes.float32)
scene1_frame1.read('flow', '../data/scene1/0000-flow.flo', dtype=itypes.float32)
scene1_frame1.read('occ', '../data/scene1/0000-occ.png', dtype=itypes.bool)

scene1_frame2 = TorchStruct(dims = "bchw", device=device)
scene1_frame2.read('image0', '../data/scene1/0001-image0.png', dtype=itypes.float32)
scene1_frame2.read('image1', '../data/scene1/0001-image1.png', dtype=itypes.float32)
scene1_frame2.read('flow', '../data/scene1/0001-flow.flo', dtype=itypes.float32)
scene1_frame2.read('occ', '../data/scene1/0001-occ.png', dtype=itypes.bool)

scene2_frame1 = TorchStruct(dims = "bchw", device=device)
scene2_frame1.read('image0', '../data/scene2/0000-image0.png', dtype=itypes.float32)
scene2_frame1.read('image1', '../data/scene2/0000-image1.png', dtype=itypes.float32)
scene2_frame1.read('flow', '../data/scene2/0000-flow.flo', dtype=itypes.float32)
scene2_frame1.read('occ', '../data/scene2/0000-occ.png', dtype=itypes.bool)

print()
print("Example torch struct scene1_frame1:")
print(scene1_frame1)

# Create dataset
ds = Dataset(file='out_write_from_structs/data.json', auto_write=True)

# First row: show images
with ds.viz.new_row() as row:
    row.add_cell('image', var='image0')
    row.add_cell('image', var='image1')
    row.add_cell('flow',  var='flow')

# Second row: show flow and occlusions
with ds.viz.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', var='occ')

# Write the data to the sequence
with ds.seq.group("scene1") as scene1:
    with scene1.item("frame1") as frame1:
        # The following will transfer all the variables that are present in ds from the TorchStruct
        frame1.set_struct(scene1_frame1)

    with scene1.item("frame2") as frame2:
        # The following will transfer all the variables that are present in ds from the TorchStruct
        frame2.set_struct(scene1_frame2)

with ds.seq.group("scene2") as scene2:
    with scene2.item("frame1") as frame1:
        # The following will transfer all the variables that are present in ds from the TorchStruct
        frame1.set_struct(scene2_frame1)

print()
print("To view run: \"iviz out_write_from_structs/data.json\"")
print()
