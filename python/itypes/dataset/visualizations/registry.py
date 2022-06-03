#!/usr/bin/env python3

_visualization_types = {}
def register_visualization(type, visualization_class):
    global _visualization_types
    _visualization_types[type] = visualization_class

def _instantiate_visualization(ds, path, type):
    global _visualization_types

    if type not in _visualization_types:
        raise Exception(f"Unknown visualization type: \"{type}\"")

    reg = ds._reg
    reg.remove(path)
    reg[path + "type"] = type

    return _visualization_types[type](ds, path)
