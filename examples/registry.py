#!/usr/bin/env python3

### --------------------------------------- ###
### Part of iTypes                          ###
### (C) 2022 Eddy ilg (me@eddy-ilg.net)     ###
### MIT License                             ###
### See https://github.com/eddy-ilg/itypes  ###
### --------------------------------------- ###

from itypes import Registry


reg = Registry('out_registry/data.json')

reg.from_dict({"foo":1, "bar":2, "fiddle":{"bar":2, "foo": [2, 3]}})

print("Keys:")
for key in reg.keys():
    print(key)
print()

print(f"reg['fiddle/bar'] = {reg['fiddle/bar']}")
print()

reg['a/b/c'] = 5
print(f"after reg['a/b/c'] = 5:")
print(reg)
print()

del reg['a/b/c']
print(f"after del reg['a/b/c']:")
print(reg)
print()

reg[(3,1)] = 5
print(f"after reg[(3,1)] = 5:")
print(reg)
print()

reg.write()

del reg[(3,1)]
print(f"after del reg[(3,1)]:")
print(reg)
print()

reg['a/b/c'] = 5
print(f"after reg['a/b/c'] = 5:")
print(reg)
print()

del reg['a/x']
print(f"after del reg['a/x']:")
print(reg)
print()

reg.write()