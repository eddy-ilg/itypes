#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

import numpy as np

from itypes import NumpyStruct

print()

s = NumpyStruct(dims="hwc")
s.x = np.array([[[1, 2, 3], [4, np.nan, np.inf]]])
s.y = NumpyStruct(dims="hwc")
s.y.z = np.array([[7, 8, 9], [10, np.nan, np.inf]])
print("s:")
print(s)
print('s.x:')
print(s.x)
print('s.y.z:')
print(s.y.z)
print()


print('nan_to_num result:')
# NOTE: s is unchanged
q = s.nan_to_num()
print("q:")
print(q)
print('q.x:')
print(q.x)
print('q.y.z:')
print(q.y.z)
print()


print("to_hwc result:")
# NOTE: s is unchanged
q = s.to_hwc()
print("q:")
print(q)
print()


print("to_chw result:")
# NOTE: s is unchanged
q = s.to_chw()
print("q:")
print(q)
print()


print("to_bhwc result:")
# NOTE: s is unchanged
q = s.to_bhwc()
print("q:")
print(q)
print()


print("to_bchw result:")
# NOTE: s is unchanged
q = s.to_bchw()
print("q:")
print(q)
print()


s = s.to_bchw()
s.int_value = 2
q = s.concat_batch([s, s])
print("after concat batch:")
print(q)
print()


print('after modify:')
q.int_value[0] = 5
q.float_value = 2.3
print(q)
print()


a, b = q.split_batch()
print('split_batch first entry:')
print(a)
print('split_batch second entry:')
print(b)
print()
