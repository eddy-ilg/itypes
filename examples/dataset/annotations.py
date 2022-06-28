#!/usr/bin/env python3

#
# The following example shows how to create a dataset with annotations.
#

from itypes import Dataset, Properties

# Create dataset
ds = Dataset(file='out_annotations/data.json', auto_write=True, structured_output=False)

# Create visualization
with ds.viz.new_row() as row:
    row.add_cell("image", var="image", props="image.props")

with ds.seq.group() as group:
    with group.item(label="Item 1") as item:
        item["image"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")

        props = Properties()
        props.ann.create("line", x0=10, y0=10, x1=500, y1=500, color="#FF0000", alpha=0.5, lw=10, ls="--")

        item["image.props"].set_data(props)


print()
print("To view run: \"iviz out_annotations/data.json\"")
print()
