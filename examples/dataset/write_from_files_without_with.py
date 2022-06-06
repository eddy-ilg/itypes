#!/usr/bin/env python3

#
# The following example shows how to create a dataset from
# existing files, omitting "with" statements as required in nested code.
#

from itypes import Dataset

# Create dataset
ds = Dataset(file='out_write_from_files_without_with/data.json')

# First row: show images and flow
row = ds.viz.new_row()
row.add_cell('image', var='image0')
row.add_cell('image', var='image1')
row.add_cell('flow',  var='flow')

# Second row: show occlusions
row = ds.viz.new_row()
row.skip_cell()
row.skip_cell()
row.add_cell('image', var='occ')

# Create a group
group = ds.seq.group('Scene-001')
item = group.item()
item['image0'].set_ref('../data/scene1/0000-image0.png', rel_to="cwd")
item['image1'].set_ref('../data/scene1/0000-image1.png', rel_to="cwd")
item['flow'].set_ref('../data/scene1/0000-flow.flo', rel_to="cwd")
item['occ'].set_ref('../data/scene1/0000-occ.png', rel_to="cwd")
item = group.item()
item['image0'].set_ref('../data/scene1/0001-image0.png', rel_to="cwd")
item['image1'].set_ref('../data/scene1/0001-image1.png', rel_to="cwd")
item['flow'].set_ref('../data/scene1/0001-flow.flo', rel_to="cwd")
item['occ'].set_ref('../data/scene1/0001-occ.png', rel_to="cwd")

# Create another group
group = ds.seq.group('Scene-002')
item = group.item()
item['image0'].set_ref('../../data/scene2/0000-image0.png', rel_to="output")
item['image1'].set_ref('../../data/scene2/0000-image1.png', rel_to="output")
item['flow'].set_ref('../../data/scene2/0000-flow.flo', rel_to="output")
item['occ'].set_ref('../../data/scene2/0000-occ.png', rel_to="output")

# NOTE: using auto_write only works with "with".
# As "with" is not used here, we have to write the data.json file manually.
ds.write()

print()
print("To view run: \"iviz out_write_from_files_without_with/data.gridseq\"")
print()






