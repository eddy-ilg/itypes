#!/usr/bin/env python3

import numpy as np
from itypes import Path, File
import torch

print()

def test_read(file, **kwargs):
    data = File(f"../data/{file}").read(**kwargs)
    cmd = f"File('../data/{file}').read({kwargs}):"
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}, device={data.device}")

def test_read_write(file, **kwargs):
    data = File(f"../data/{file}").read(**kwargs)
    cmd = f"File('../data/{file}').read({kwargs}):"
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}, device={data.device}")
    cmd = f"After write:"

    File(f"out_read_write_torch/{file}").write(data)
    data = File(f"out_read_write_torch/{file}").read(device=kwargs["device"])
    print(f"{cmd:80s}  shape={data.shape}, dtype={data.dtype}, min={data.min()}, max={data.max()}, device={data.device}")

test_read('test-rgb.png', device=torch.device("cpu"))
test_read('test-rgb.png', device=torch.device("cuda:0"))
print()

test_read_write('test-rgb.png', device=torch.device("cpu"))
test_read_write('test-rgb.png', device=torch.device("cuda:0"))
print()

Path("out_read_write_torch").remove()