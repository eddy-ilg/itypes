#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# Read dataset
#
import itypes
from itypes import Dataset, psep

ds = Dataset("out_perf_test_write/data.json").read()

print(f'Datatset length: {len(ds)}')
print()

psep("Groups:")
print(ds.seq.group_list())
psep()
print()

psep("Items from first group:")
print(ds.seq.item_list(ds.seq.group_list()[0][0]))
psep()