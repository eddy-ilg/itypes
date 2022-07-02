#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import Path, home

path = Path('../data')
print()

# Home
print(f'home: {home}')
print()

# List directories
print("Path('../data').list_dirs():")
for ent in path.list_dirs():
    print(f"  '{str(ent)}', type={type(ent)}")
print()

# List files
print("Path('../data').list_files():")
for ent in path.list_files():
    print(f"  '{str(ent)}', type={type(ent)}")
print()

# cd, abs, part, name
path = Path('.').cd('../data')
print(f"Path('.').cd('../data'):               {path}")
print(f"Path('.').cd('../data').abs():         {path.abs()}")
print(f"Path('.').cd('../data').abs().part(2): {path.abs().part(2)}")
print(f"Path('.').cd('../data').abs().name():  {path.abs().name()}")
print("Note that part(0) is the '' before the first slash.")
print()

# mkdir
path = Path('output/mkdir')
path.mkdir()
print(f"path.exists() after mkdir:  {path.exists()}")
print(f"path.empty()  after mkdir:  {path.empty()}")
path.file("test.txt").write("Test Content")
print(f"path.empty()  after write:  {path.empty()}")
path.remove()
print(f"path.exists() after remove: {path.exists()}")
Path("output").remove()
print()

# rel_to
path1 = Path('../data')
path2 = Path('../data').cd('subdir1').cd('subdir2')
path3 = Path('../data').cd('subdir1').cd('subdir2').abs()
print(f"path1: {path1}")
print(f"path2: {path2}")
print(f"path3: {path3}")
print(f"path1.rel_to(path_2): '{path1.rel_to(path2)}'")
print(f"path1.rel_to(path_3): '{path1.rel_to(path3)}'")
print(f"path2.rel_to(path_1): '{path2.rel_to(path1)}'")
print(f"path2.rel_to(path_3): '{path2.rel_to(path3)}'")
print(f"path3.rel_to(path_1): '{path3.rel_to(path1)}'")
print(f"path3.rel_to(path_2): '{path3.rel_to(path2)}'")
print()

# index(), str_index()
path = Path('../data').cd('test-00003')
print(f"Path('../data').cd('test-00003').index():     {path.index()}")
print(f"Path('../data').cd('test-00003').str_index(): {path.str_index()}")
print()


# Todo equal
# Todo add move
# Todo add copy