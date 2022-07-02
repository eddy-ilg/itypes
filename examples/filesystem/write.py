#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

import numpy as np
from itypes import File, Path

print()

def test(file, **kwargs):
    data = File(f"../data/{file}").read(**kwargs)
    cmd = f"File('../data/{file}').read({kwargs}):"
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}")
    cmd = f"After write:"

    write_args = {}
    if "dims" in kwargs: write_args["dims"] = kwargs["dims"]
    File(f"out_write/{file}").write(data, **write_args)
    data = File(f"out_write/{file}").read()
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}")


test('test-rgb.png')
test('test-rgb.png', alpha=True)
test('test-rgb.png', dtype=np.float32)
print()

test('test-rgba.png')
test('test-rgba.png', alpha=False)
print()

test('test-gray16.png')
test('test-gray16.png', dtype=np.uint8)
test('test-gray16.png', dtype=np.float32)
print()

test('test-mask.png')
test('test-mask.png', dtype=np.uint8)
test('test-mask.png', dtype=np.uint16)
test('test-mask.png', dtype=np.float32)
print()

test('test-mask.png')
test('test-mask.png', dtype=np.uint8)
test('test-mask.png', dtype=np.uint16)
test('test-mask.png', dtype=np.float32)
print()

test('test.pfm')
print()

test('test.flo')
print()

test('test-rgb.png', dims="hwc")
test('test-rgb.png', dims="chw")
test('test-rgb.png', dims="bhwc")
test('test-rgb.png', dims="bchw")
print()

Path("out_write").remove()