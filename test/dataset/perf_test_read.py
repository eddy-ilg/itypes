#!/usr/bin/env python3

#
# Read dataset
#
import itypes
from itypes import Dataset

ds = Dataset("out_perf_test_write/data.json").read()

print(f'datatset length: {len(ds)}')
