#!/usr/bin/env python3

#
# The following example shows how to create a dataset from
# existing files.
#

from itypes import Dataset

# Create sequence
ds = Dataset(file='out_write_from_files/data.json', auto_write=True)

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

# Create a scene with frames
with ds.seq.group('Scene-001') as group:
    with group.item() as item:
        item["image0"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene1/0000-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene1/0000-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene1/0000-occ.png', rel_to="cwd")
    with group.item() as item:
        item["image0"].set_ref('../data/scene1/0001-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene1/0001-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene1/0001-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene1/0001-occ.png', rel_to="cwd")

with ds.seq.group('Scene-002') as group:
    with group.item() as item:
        item["image0"].set_ref('../data/scene2/0000-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene2/0000-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene2/0000-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene2/0000-occ.png', rel_to="cwd")

print()
print("To view run: \"iviz out_write_from_files/data.json\"")
print()
