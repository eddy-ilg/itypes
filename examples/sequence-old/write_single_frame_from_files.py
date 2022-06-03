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
# The following example shows how to conveniently fill in a single frame sequence directly/
#
from itypes import Sequence

# NOTE: Since a filename is specified here, any new images will be written to disk immediately
# to the path containing the data.json file
seq = Sequence(filename='out_write_single_frame_from_files/data.json', single_frame=True)

# First row: show images
with seq.grid.new_row() as row:
    row.add_cell('image', 'image0').set_ext('../data/scene1/0000-image0.png')
    row.add_cell('image', 'image1').set_ext('../data/scene1/0000-image1.png')
    row.add_cell('flow',  'flow').set_ext('../data/scene1/0000-flow.flo')

# Second row: show flow and occlusions
with seq.grid.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell('image', 'occ').set_ext('../data/scene1/0000-occ.png')

seq.write()
seq.write(filename='out_write_single_frame_from_files/data.gridseq')

print()
print("To view run: \"iviz out_write_single_frame_from_files/data.gridseq\"")
print()







