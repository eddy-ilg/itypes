#!/usr/bin/env python3

# This is a helper class to keep a
# reference to the linear index, as
# it may change centrally in case of
# fragmented scene writes
class _LinearIndex:
    def __init__(self, value=None):
        self._value = value

    def set_value(self, value):
        self._value = value

    def value(self):
        return self._value

class DataIndex:
    def __init__(self, scene, frame, id, linear_index=None):
        self._scene = scene
        self._frame = frame
        self._id = id
        self._linear_index = linear_index

    def id(self): return self._id
    def scene(self): return self._scene
    def frame(self): return self._frame
    def linear_index(self): return self._linear_index.value() if self._linear_index is not None else None

    def __str__(self):
        if self._linear_index is not None:
            return f"DataIndex(id={self._id}, scene={self._scene}, frame={self._frame}, linear_index={self._linear_index.value()})"
        else:
            return f"DataIndex(id={self._id}, scene={self._scene}, frame={self._frame})"
