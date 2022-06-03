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
# The following example shows how to create a sequence from
# torch structs that are already in memory.
#

#
# Actual example
#
import torch
import itypes
from itypes import Sequence, TorchStruct

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
print("Example torch struct (scene1_frame1):")
print(scene1_frame1)

# Create sequence with two colums
# NOTE: Since a filename is specified here, any new images will be written to disk immediately
# to the path containing the data.json file
seq = Sequence(filename='out_write_from_struct/data.json')

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
with seq.data.scene("scene1") as scene1:
    with scene1.sample("frame1") as frame1:
        # The following will transfer all the ids that are present in seq from the TorchStruct
        frame1.set_struct(scene1_frame1)

    with scene1.sample("frame2") as frame2:
        # The following will transfer all the ids that are present in seq from the TorchStruct
        frame2.set_struct(scene1_frame2)

with seq.data.scene("scene2") as scene2:
    with scene2.sample("frame1") as frame1:
        # The following will transfer all the ids that are present in seq from the TorchStruct
        frame1.set_struct(scene2_frame1)

    with scene2.sample("frame2") as frame2:
        # The following will transfer all the ids that are present in seq from the TorchStruct
        frame2.set_struct(scene1_frame2)

# Write the sequence
seq.write()
seq.write(filename='out_write_from_struct/data.gridseq')

print()
print("To view run: \"iviz out_write_from_struct/data.gridseq\"")
print()
