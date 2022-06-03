#!/usr/bin/env python3

from .filesystem import File
from copy import deepcopy

MAX_INT = 2**16 - 1


class RegistryPath:
    def __init__(self, *args):
        if len(args) == 1:
            arg = args[0]
            if isinstance(arg, str):
                self._path = list(arg.split('/'))
            else:
                self._path = list(arg._path)
        else:
            self._path = list(args)

    def __repr__(self):
        return '/'.join(self._path)

    def copy(self):
        return deepcopy(self)

    def path(self):
        return deepcopy(self._path)

    def append(self, *args):
        copy = self.copy()
        for arg in args:
            if arg == '..': copy._path.pop()
            else: copy._path.append(str(arg))
        return copy

    def __add__(self, other):
        if isinstance(other, RegistryPath):
            return self.append(other._path)
        else:
            return self.append(other)

    def sub_key(self):
        copy = self.copy()
        copy._path.pop(0)
        return copy

    def __getitem__(self, index):
        return self._path[index]

    def __len__(self):
        return len(self._path)

# def _container_keys(root, d, max_depth=MAX_INT):
#     keys = []
#     if max_depth == 0:
#         return keys
#
#     for key , value in d.items():
#         sub_key = root.append(key)
#         if isinstance(value, dict):
#             keys += _keys(sub_key, value, max_depth - 1)
#         else:
#             keys.append(sub_key)
#
#     return keys
#
# def _value_keys(root, d, max_depth=MAX_INT):
#     keys = []
#     if max_depth == 0:
#         return keys
#
#     for key , value in d.items():
#         sub_key = root.append(key)
#         if isinstance(value, dict):
#             keys += _keys(sub_key, value, max_depth - 1)
#         else:
#             keys.append(sub_key)
#
#     return keys

def _getitem(d, key):
    if len(key) == 0:
        return d

    if len(key) == 1:
        return d[str(key)]

    sub_key = key.sub_key()
    current_key = str(key[0])
    return _getitem(d[current_key], sub_key)

def _contains(d, key):
    if len(key) == 0:
        raise Exception(f"empty key encountered in _contains")

    if len(key) == 1:
        return str(key) in d

    sub_key = key.sub_key()
    current_key = str(key[0])
    if current_key not in d:
        return False
    return _contains(d[current_key], sub_key)

def _setitem(d, key, value, dict_class=dict):
    if len(key) == 0:
        raise Exception(f"empty key encountered in _setitem")

    if len(key) == 1:
        d[str(key)] = value
        return

    sub_key = key.sub_key()
    current_key = str(key[0])
    if current_key not in d:
        d[current_key] = dict_class()
    _setitem(d[current_key], sub_key, value)

def _delitem(d, key):
    if len(key) == 0:
        raise Exception(f"empty key encountered in _delitem")

    if len(key) == 1:
        if str(key) in d:
            del d[str(key)]
        return

    sub_key = key.sub_key()
    current_key = str(key[0])
    if current_key not in d:
        return

    _delitem(d[current_key], sub_key)

    if len(d[current_key]) == 0:
        del d[current_key]

class Registry(dict):
    def __init__(self, file=None):
        self._file = file

    def to_dict(self):
        return dict(deepcopy(self))

    def from_dict(self, data):
        self.clear()
        self.update(data)

    def read(self, file=None):
        if file is None:
            file = self._file
        self.clear()
        self.update(File(file).read())
        self._file = file

    def write(self, file=None):
        if file is None:
            file = self._file
        File(file).write(self)
        self._file = file

    def __getitem__(self, key):
        if '/' not in str(key):
            return super().__getitem__(str(key))
        key = RegistryPath(key)
        return _getitem(self, key)

    def __setitem__(self, key, value):
        if '/' not in str(key):
            return super().__setitem__(str(key), value)
        key = RegistryPath(key)
        return _setitem(self, key, value)

    def remove(self, key):
        if '/' not in str(key):
            if not str(key) in self:
                return
            return super().__delitem__(str(key))
        key = RegistryPath(key)
        return _delitem(self, key)

    def __delitem__(self, key):
        self.remove(key)

    def __contains__(self, key):
        if '/' not in str(key):
            return super().__contains__(str(key))
        key = RegistryPath(key)
        return _contains(self, key)