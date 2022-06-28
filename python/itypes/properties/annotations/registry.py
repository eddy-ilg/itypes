#!/usr/bin/env python3

_annotation_types = {}
def register_annotation(type, annotation_class):
    global _annotation_types
    _annotation_types[type] = annotation_class

def _instantiate_annotation(type, props, path, **kwargs):
    global _annotation_types

    if type not in _annotation_types:
        raise Exception(f"Unknown annotation type: \"{type}\"")

    type = _annotation_types[type](props, path)
    type.create(**kwargs)

    return type 

def _reinstantiate_annotation(props, path):
    global _annotation_types

    reg = props._reg
    type = reg[path + "type"]

    if type not in _annotation_types:
        raise Exception(f"Unknown annotation type: \"{type}\"")

    return _annotation_types[type](props, path)
