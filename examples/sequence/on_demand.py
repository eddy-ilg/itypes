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
# The following example how data can be supplied to sequences
# "on-demand" by proving a function that is called by the sequence
# when it actually needs the data.
# NOTE: together with keeping sequences in memory only, this allows
# to connect iviz to any existing data structures you have in memory
# and directly visualize them.
#


#
# Actual example
#
import itypes
from itypes import File, Sequence

# Read data into memory
device = "numpy"  # Note: this works with torch devices as well

def get_data_item(index):
    # If iviz needs the data, it will call this function.
    # In the example the data is read from disk. However,
    # note that data could be generated here on the fly
    # when it is requested.

    if index.scene() == "scene1": scene_id = "1"
    else:                         scene_id = "2"
    if index.frame() == "frame1": frame_id = "0000"
    else:                         frame_id = "0001"

    # NOTE: this has to return the dims that were given
    # in set_data(), by default "hwc"

    if index.id() == "image0":
        return File(f'../data/scene{scene_id}/{frame_id}-{index.id()}.png').\
            read(dtype=itypes.float32, device=device, dims="hwc")
    elif index.id() == "image1":
        return File(f'../data/scene{scene_id}/{frame_id}-image1.png').\
            read(dtype=itypes.float32, device=device, dims="hwc")
    elif index.id() == "flow":
        return File(f'../data/scene{scene_id}/{frame_id}-flow.flo').\
            read(dtype=itypes.float32, device=device, dims="hwc")
    elif index.id() == "occ":
        return File(f'../data/scene{scene_id}/{frame_id}-occ.png').\
            read(dtype=itypes.bool, device=device, dims="hwc")


# Create sequence
# NOTE: since there is no filename specified here, the entire data will be kept in memory
# and only written once seq.write() is called
seq = Sequence()

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
with seq.data.scene('scene1') as scene:
    with scene.sample("frame1") as frame:
        frame.set_data('image0', get_data_item)
        frame.set_data('image1', get_data_item)
        frame.set_data('flow', get_data_item)
        frame.set_data('occ', get_data_item)
    with scene.sample("frame2") as frame:
        frame.set_data('image0', get_data_item)
        frame.set_data('image1', get_data_item)
        frame.set_data('flow', get_data_item)
        frame.set_data('occ', get_data_item)

# Create another scene
with seq.data.scene('scene2') as scene:
    with scene.sample("frame1") as frame:
        frame.set_data('image0', get_data_item)
        frame.set_data('image1', get_data_item)
        frame.set_data('flow', get_data_item)
        frame.set_data('occ', get_data_item)

# TODO
# In future you will be able to directly visualize the data without ever writing it to disk:
# iviz.visualize(seq)

# Generate the data now and write the entire sequence to disk.
# This will write data.gridseq and the images.
seq.write(filename='out_on_demand/data.gridseq')

print()
print("To view run: \"iviz out_on_demand/data.gridseq\"")
print()







