#!/usr/bin/env python3

#
# Configure logging
#
import logging
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--debug", action="store_true", help="Show debugging output.")
args = parser.parse_args()
log_level = logging.DEBUG if args.debug else logging.INFO
logging.basicConfig(level=log_level, format='[%(levelname)8s] %(name)-15s : %(message)s')

#
# The following example shows how write a sequence
# with a linear output folder structure.
#

#
# Actual example
#
import itypes
from itypes import File, Sequence

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

# Create sequence with two rows
# NOTE: Since a filename is specified here, any new images will be written to disk immediately
# to the path containing the data.json file
seq = Sequence(filename='out_write_from_tensor_linear/data.json', structured_output=False)

# First row: show images
with seq.grid.new_row() as row:
    row.add_cell('image', 'image0')
    row.add_cell('image', 'image1')
    row.add_cell('flow',  'flow')

# Second row: show flow and occlusions
with seq.grid.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', 'occ')

# Write the data to the sequence
for scene_name, scene_dict in data.items():
    scene = seq.data.scene(scene_name)
    for frame_name, frame_dict in scene_dict.items():
        frame = scene.sample(frame_name)
        for id, tensor in frame_dict.items():
            frame.set_data(id, tensor, dims="bchw")

seq.write()
seq.write(filename='out_write_from_tensor_linear/data.gridseq')

print()
print("To view run: \"iviz out_write_from_tensor_linear/data.gridseq\"")
print()







