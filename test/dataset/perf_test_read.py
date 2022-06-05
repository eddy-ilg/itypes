#!/usr/bin/env python3

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