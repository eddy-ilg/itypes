#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# This script writs 3 pixels with colors R, G, B.
# Check in your native viewer if the pixels appear correctly.
#

import numpy as np
from itypes import File

data = np.zeros((3, 3, 3), dtype=np.float32)

# First pixel is red
data[:, 0, 0] = 1.0
data[:, 0, 1] = 0
data[:, 0, 2] = 0

# Second pixel is green
data[:, 1, 0] = 0
data[:, 1, 1] = 1.0
data[:, 1, 2] = 0

# Third pixel is blue
data[:, 2, 0] = 0
data[:, 2, 1] = 0
data[:, 2, 2] = 1.0

File('out_color_test/image.png').write(data, dims="hwc")

read_data = File('out_color_test/image.png').read(dims="hwc", dtype=np.float32)

print()
print("Read data is equal to written data:", np.array_equal(data, read_data))
print("Check out_color_test/image.png with your native viewer, if pixels are R,G,B.")
print()