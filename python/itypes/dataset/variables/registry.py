#!/usr/bin/env python3

_variable_types = {}
def register_variable(type, variable_class):
    global _variable_types
    _variable_types[type] = variable_class

def _instantiate_variable(type, ds, path, **kwargs):
    global _variable_types

    if type not in _variable_types:
        raise Exception(f"Unknown variable type: \"{type}\"")

    return _variable_types[type](ds, path, **kwargs)
