#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import File
from itypes.filesystem.memory import MemoryFileSystem

mfs = MemoryFileSystem('/memory')

mfs.read_from_disk('../data')

print('Initial mfs:')
print(mfs, end='')

data = File('/memory/test-rgb.png').read()
print(f'Read test-rgb.png with size {data.shape}')

print('/memory/test-rgb-writeback.png exists:', File('/memory/test-rgb-writeback.png').exists())

File('/memory/test-rgb-writeback.png').write(data)

print('/memory/test-rgb-writeback.png exists:', File('/memory/test-rgb-writeback.png').exists())

f = File("/memory/test.txt").open('w')
f.write("test")
f.close()

f = File("/memory/test.txt").open('r')
print(f"Read-back of test.txt: \"{f.read()}\"")

print('After writing:')
print(mfs, end='')

data = File('/memory/test-rgb-writeback.png').read()
print(f'Read test-rgb-writeback.png with size {data.shape}')

mfs.write_to_disk('out_memory')