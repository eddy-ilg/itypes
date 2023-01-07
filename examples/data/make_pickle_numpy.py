#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

import numpy as np
import pickle
from PIL import Image

def read_image(url):
    with open(url, "rb") as f:
        d = np.asarray(Image.open(f))
        if len(d.shape) == 3 and d.shape[2]>3:
            d = d[:, :, 0:3]
        return d.squeeze().astype(np.float32)/255

def write_numpy(url, data):
    with open(url, "wb") as f:
        np.save(f, data, allow_pickle=True)

def write_numpy_compressed(url, data):
    with open(url, "wb") as f:
        np.savez_compressed(f, data, allow_pickle=True)

def write_pickle(url, data):
    with open(url, "wb") as f:
        pickle.dump(data, f)

t1 = np.array([
    [1.1, 2.3, 3.9],
    [4.2, 5.8, 6.1]
], dtype=float)
print('t1:', t1.shape, t1.dtype)
print(t1)

t2 = np.array([
    [1.1, 2.3, 3.9],
    [4.2, 5.8, 6.1]
], dtype=np.uint8)
print('t2:', t2.shape, t2.dtype)
print(t2)

t3 = read_image('test-rgb.png')
print('t3:', t3.shape, t3.dtype)


data = {'t1': t1, 't2': t2, "t3": t3}
write_numpy('test.npy', data)
write_numpy_compressed('test.npz', data)
write_pickle('test.p', data)

write_numpy_compressed('test-direct.npz', t1) 
