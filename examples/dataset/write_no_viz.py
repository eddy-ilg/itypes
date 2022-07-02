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

from itypes import Dataset

# Create sequence
ds = Dataset(file='out_write_no_viz/data.json', auto_write=True)

# Create variables instead of visualizations
ds.var.create("image", "image0")
ds.var.create("image", "image1")
ds.var.create("image", "flow")
ds.var.create("image", "occ")

# Create a scene with two frames
with ds.seq.group('scene_001', label="Scene 1") as group:
    with group.item("item_001", label="Item 1") as item:
        item["image0"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene1/0000-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene1/0000-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene1/0000-occ.png', rel_to="cwd")
    with group.item("item_002", label="Item 2") as item:
        item["image0"].set_ref('../data/scene1/0001-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene1/0001-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene1/0001-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene1/0001-occ.png', rel_to="cwd")

# Create another scene with one frame
with ds.seq.group('scene_002', label="Scene 2") as group:
    with group.item("item_001", label="Item 1") as item:
        item["image0"].set_ref('../data/scene2/0000-image0.png', rel_to="cwd")
        item["image1"].set_ref('../data/scene2/0000-image1.png', rel_to="cwd")
        item["flow"].set_ref('../data/scene2/0000-flow.flo', rel_to="cwd")
        item["occ"].set_ref('../data/scene2/0000-occ.png', rel_to="cwd")

print()
print("To view run: \"iviz out_write_no_viz/data.json\"")
print()
