#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

import numpy as np
from itypes import read_parallel

# This will execute all reads in parallel and block
# until the reads are done
data = read_parallel([
    "../data/test-rgb.png",
    "../data/test-rgba.png",
    "../data/test-mask.png"
], dtype=np.float32)

print()
print("Read data:")
for entry in data:
    print(f"  shape={entry.shape}, dtype={entry.dtype}, min={entry.min()}, max={entry.max()}")
print()
