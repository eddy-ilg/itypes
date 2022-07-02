#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# The following example shows how to create a dataset with annotations.
#

from itypes import Dataset, Properties

# Create dataset
ds = Dataset(file='out_annotations/data.json', auto_write=True, structured=False)

# Create visualization
with ds.viz.new_row() as row:
    row.add_cell("image", var="image", props="image.props")

with ds.seq.group() as group:
    with group.item(label="Shapes") as item:
        item["image"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")

        props = Properties()
        props.ann.create("line", x0=10, y0=10, x1=500, y1=500, color="#FF0000", alpha=0.5, lw=10, ls="--")
        props.ann.create("rect", x0=250, y0=10, x1=750, y1=500, color="#00FF00", alpha=0.5, lw=10, ls=".")
        props.ann.create("circle", x=500, y=250, r=100, color="#0000FF")

        item["image.props"].set_data(props)

    with group.item(label="Ellipses") as item:
        item["image"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")

        props = Properties()
        props.ann.create("mark", x=250, y=250)
        props.ann.create("ellipse", x=250, y=250, r0=150, r1=75, color="#0000FF")
        props.ann.create("mark", x=750, y=250)
        props.ann.create("ellipse", x=750, y=250, r0=150, r1=75, a=3.14/4, color="#0000FF")

        item["image.props"].set_data(props)

    with group.item(label="Marks") as item:
        item["image"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")

        props = Properties()
        for i in range(0, 15):
            props.ann.create("mark", x=50 + 50*i, y=50, size=5 + i, shape="+")
            props.ann.create("mark", x=50 + 50*i, y=100, size=5 + i, shape="x")
            props.ann.create("mark", x=50 + 50*i, y=150, size=5 + i, shape="^")
            props.ann.create("mark", x=50 + 50*i, y=200, size=5 + i, shape="s")
            props.ann.create("mark", x=50 + 50*i, y=250, size=5 + i, shape="o")

        item["image.props"].set_data(props)

    with group.item(label="Text") as item:
        item["image"].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")

        props = Properties()
        def draw_text(x, y, halign, valign, color="#FFFFFF"):
            props.ann.create("mark", x=x, y=y, color="#FF0000")
            props.ann.create("text", x=x, y=y, text="test", size=30, halign=halign, valign=valign, color=color)

        draw_text(100, 100, "right", "bottom")
        draw_text(200, 100, "center", "bottom")
        draw_text(300, 100, "left", "bottom")

        draw_text(100, 200, "right", "center")
        draw_text(200, 200, "center", "center", color="#00FF00")
        draw_text(300, 200, "left", "center")

        draw_text(100, 300, "right", "top")
        draw_text(200, 300, "center", "top")
        draw_text(300, 300, "left", "top")

        props.ann.create("box", x0=500, y0=150, x1=700, y1=350, text="test", size=20, color="#00FF00")

        item["image.props"].set_data(props)


print()
print("To view run: \"iviz out_annotations/data.json\"")
print()
