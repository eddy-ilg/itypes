#!/usr/bin/env python3

import numpy as np
from itypes import Path, File

# file = File("data/test.p")
# print(f"data/test.p: {file.read()}")

print()

def test(file, **kwargs):
    data = File(f"../data/{file}").read(**kwargs)
    cmd = f"File('../data/{file}').read({kwargs}):"
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}")

test('test-rgb.png')
test('test-rgb.png', alpha=True)
test('test-rgb.png', alpha=False)
print()

test('test-rgba.png')
test('test-rgba.png', alpha=True)
test('test-rgba.png', alpha=False)
print()

test('test-mask.png')
test('test-mask.png', alpha=True)
test('test-mask.png', alpha=False)
print()

test('test-gray16.png')
test('test-gray16.png', alpha=True)
test('test-gray16.png', alpha=False)
print()

test('test-gray16.png', dtype=np.uint8)
test('test-gray16.png', dtype=np.uint16)
test('test-gray16.png', dtype=np.float32)
print()

test('test-rgb.png', dtype=np.uint8)
test('test-rgb.png', dtype=np.uint16)
test('test-rgb.png', dtype=np.float32)
print()

test('test-rgb.exr')
test('test-gray.exr')
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

Path("write_test").remove()