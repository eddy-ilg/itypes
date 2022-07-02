#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how write a dataset
# with a linear output folder structure.
#

import itypes
from itypes import File, Dataset

# Read data into memory
device = "numpy"  # Note: this works with torch devices as well
data = {
    "scene1": {
        "0000": {
            "image0": File('../data/scene1/0000-image0.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "image1": File('../data/scene1/0000-image1.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "flow": File('../data/scene1/0000-flow.flo').read(dtype=itypes.float32, device=device, dims="bchw"),
            "occ": File('../data/scene1/0000-occ.png').read(dtype=itypes.bool, device=device, dims="bchw"),
        },
        "0001": {
            "image0": File('../data/scene1/0001-image0.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "image1": File('../data/scene1/0001-image1.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "flow": File('../data/scene1/0001-flow.flo').read(dtype=itypes.float32, device=device, dims="bchw"),
            "occ": File('../data/scene1/0001-occ.png').read(dtype=itypes.bool, device=device, dims="bchw"),
        }
    },
    "scene2": {
        "0000": {
            "image0": File('../data/scene2/0000-image0.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "image1": File('../data/scene2/0000-image1.png').read(dtype=itypes.float32, device=device, dims="bchw"),
            "flow": File('../data/scene2/0000-flow.flo').read(dtype=itypes.float32, device=device, dims="bchw"),
            "occ": File('../data/scene2/0000-occ.png').read(dtype=itypes.bool, device=device, dims="bchw"),
        },
    }
}

# Create dataset
ds = Dataset(file='out_write_from_tensor_linear/data.json', auto_write=True, structured=False)

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
for scene_name, scene_dict in data.items():
    group = ds.seq.group(scene_name)
    for frame_name, frame_dict in scene_dict.items():
        item = group.item(frame_name)
        for id, tensor in frame_dict.items():
            item[id].set_data(tensor, dims="bchw")

print()
print("To view run: \"iviz out_write_from_tensor_linear/data.json\"")
print()







