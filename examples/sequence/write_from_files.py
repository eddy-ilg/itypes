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
# existing files.
#

#
# Actual example
#
from itypes import Sequence

# Create sequence
seq = Sequence(filename='out_write_from_files/data.json')

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

# Create a scene
with seq.data.scene('Scene-001') as scene:
    with scene.sample() as frame:
        frame.set_ext('image0', '../data/scene1/0000-image0.png', rel_to="cwd")
        frame.set_ext('image1', '../data/scene1/0000-image1.png', rel_to="cwd")
        frame.set_ext('flow', '../data/scene1/0000-flow.flo', rel_to="cwd")
        frame.set_ext('occ', '../data/scene1/0000-occ.png', rel_to="cwd")
    with scene.sample() as frame:
        frame.set_ext('image0', '../data/scene1/0001-image0.png', rel_to="cwd")
        frame.set_ext('image1', '../data/scene1/0001-image1.png', rel_to="cwd")
        frame.set_ext('flow', '../data/scene1/0001-flow.flo', rel_to="cwd")
        frame.set_ext('occ', '../data/scene1/0001-occ.png', rel_to="cwd")

# Create another scene
with seq.data.scene('Scene-002') as scene:
    with scene.sample() as frame:
        frame.set_ext('image0', '../../data/scene2/0000-image0.png', rel_to="output")
        frame.set_ext('image1', '../../data/scene2/0000-image1.png', rel_to="output")
        frame.set_ext('flow', '../../data/scene2/0000-flow.flo', rel_to="output")
        frame.set_ext('occ', '../../data/scene2/0000-occ.png', rel_to="output")

seq.write()
seq.write(filename='out_write_from_files/data.gridseq')

print()
print("To view run: iviz \"out_write_from_files/data.gridseq\"")
print()






