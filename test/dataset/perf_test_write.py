#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how to create a dataset from
# existing files.
#

import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--groups", type=int, default=1000, help="Number of groups to write.")
parser.add_argument("--items", type=int, default=1000, help="Number of items per group to write.")
args = parser.parse_args()

from itypes import Dataset
from iutils import profiler

# Create sequence
ds = Dataset(file='out_perf_test_write/data.json')

# First row: show images
with ds.viz.new_row() as row:
    row.add_cell("image", variable="image0")
    row.add_cell("image", variable="image1")
    row.add_cell("flow",  variable="flow")

# Second row: show flow and occlusions
with ds.viz.new_row() as row:
    row.skip_cell()
    row.skip_cell()
    row.add_cell("image", variable="occ")

print(f'writing {args.groups*args.items} entries (can take multiple hours)')

for i in range(0, args.groups):
    with ds.seq.group('%03d' % i) as group:
        for j in range(0, args.items):
            with profiler.scope("add item"):
                profiler.start("with group.item()")
                with group.item() as item:
                    profiler.stop("with group.item()")
                    with profiler.scope("assignments"):
                        item["image0"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")
                        item["image1"].set_ref('../data/scene1/0000-image1.png', rel_to="cwd")
                        item["flow"].set_ref('../data/scene1/0000-flow.flo', rel_to="cwd")
                        item["occ"].set_ref('../data/scene1/0000-occ.png', rel_to="cwd")
    profiler.print_summary()

ds.write()

profiler.print_final_summary()

print('done.')
