#!/usr/bin/env python3

#
# The following example shows how to iterate over variables and visualizations
#

from itypes import Dataset, psep

#
# Generate a sequence
#
import os

print()
print("Running: \"python3 ./write_from_files.py > /dev/null\"")
os.system("python3 ./write_from_files.py > /dev/null")
print()

#
# Read single items in linear mode
#
import itypes
from itypes import Dataset, psep

ds = Dataset("out_write_from_files/data.json").read()

psep("Variable names:")
print(ds.var.names())
psep()
print()

psep("Variables:")
for var in ds.var:
    print(f"type={var.type():12s} name={var.name():12s}")
psep()
print()

psep("Values for \"flow\":")
for value in ds.var["flow"]:
    print(f"type={value.type():12s} variable_name={value.variable_name():12s} group_name={value.group_name():12s} item_name={value.item_name():12s} file={value.file()}")
psep()
print()

psep("Visualizations:")
for viz in ds.viz:
    print(f"type={viz.type():12s} index={viz.index()}     variable_names={viz.variable_names()}")
psep()
print()

psep("All group names:")
print(ds.seq.group_names())
psep()
print()

psep("Item names for group \"scene_001\":")
print(ds.seq.item_names("scene_001"))
psep()
print()

psep("All groups:")
for group in ds.seq.group_list():
    print(f"index={group['index']} group_name={group['name']:12s} group_label=\"{group['label']}\"")
psep()
print()

psep("All items:")
for item in ds.seq.full_item_list():
    print(f"index={item['index']} group_name={item['group_name']:12s} item_name={item['item_name']} group_label=\"{item['group_label']}\" item_label=\"{item['item_label']}\"")
psep()
print()

psep("Item for \"Scene-001\":")
for item in ds.seq.item_list("scene_001"):
    print(f"index={item['index']} item_name={item['name']} item_label=\"{item['label']}\"")
psep()
print()
