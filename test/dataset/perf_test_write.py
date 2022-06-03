#!/usr/bin/env python3

#
# The following example shows how to create a dataset from
# existing files.
#

import sys
from itypes import Dataset

# Create sequence
ds = Dataset(file='perf_test_write/data.json')

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

print('writing 1,000,000 entries')

for i in range(0, 1000):
    with ds.seq.group('%03d' % i) as group:
        for j in range(0, 1000):
            with group.item() as item:
                item["image0"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")
                item["image1"].set_ref('../data/scene1/0000-image1.png', rel_to="cwd")
                item["flow"].set_ref('../data/scene1/0000-flow.flo', rel_to="cwd")
                item["occ"].set_ref('../data/scene1/0000-occ.png', rel_to="cwd")
    print('.', end='')
    sys.stdout.flush()

ds.write()

