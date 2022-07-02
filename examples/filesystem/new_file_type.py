#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

#
# Register a new file type with extension ".myfile"
#
from itypes.filesystem.io import register_read_function, register_write_function

def read_myfile(filename):
    print("Reading from .myfile file")
    with open(filename, "r") as f:
        return f.read()

register_read_function("myfile", read_myfile)

def write_myfile(filename, data):
    print("Writing to .myfile file")
    with open(filename, "w") as f:
        f.write(data)

register_write_function("myfile", write_myfile)


#
# Write and read to .myfile files
#
from itypes import File

file = File('out_new_file_type/test.myfile')\

file.write("some content")
data = file.read()

print(f"Read: \"{data}\"")


