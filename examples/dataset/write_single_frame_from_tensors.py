#!/usr/bin/env python3

# The following example shows how to conveniently fill in a single frame sequence directly.
#
import itypes
from itypes import File, Dataset

# Read data into memory
device = "numpy" # Note: this could be "cuda" as well
image0 = File('../data/scene1/0000-image0.png').read(dtype=itypes.float32, device=device, dims="bchw")
image1 = File('../data/scene1/0000-image1.png').read(dtype=itypes.float32, device=device, dims="bchw")
flow = File('../data/scene1/0000-flow.flo').read(dtype=itypes.float32, device=device, dims="bchw")
occ = File('../data/scene1/0000-occ.png').read(dtype=itypes.bool, device=device, dims="bchw")

# Create dataset with a single item
ds = Dataset(file='out_write_single_frame_from_tensors/data.json', single_item=True, auto_write=True)

# First row: show images
with ds.viz.new_row() as row:
    row.add_cell('image', var='image0').set_data(image0, dims="bchw")
    row.add_cell('image', var='image1').set_data(image1, dims="bchw")
    row.add_cell('flow',  var='flow').set_data(flow, dims="bchw")

# Second row: show flow and occlusions
with ds.viz.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', var='occ').set_data(occ, dims="bchw")

print()
print("To view run: \"iviz out_write_single_frame_from_tensors/data.json\"")
print()
