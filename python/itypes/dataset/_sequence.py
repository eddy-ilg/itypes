#!/usr/bin/env python3

from ._group import _Group
from ..registry import RegistryPath


class _Iterator:
    def __init__(self, seq):
        self._seq = seq
        self._groups = seq.group_names()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._groups):
            raise StopIteration

        value = self._seq[self._groups[self._index]]
        self._index += 1
        return value


class _Sequence:
    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("sequence")

    def group(self, name="default", title=None):
        if title is None:
            title = name
        path = self._path + "groups" + name
        return _Group(self._ds, path, title)

    def group_names(self):
        path = self._path + "groups"
        return list(self._reg[path].keys())

    def __getitem__(self, name):
        path = self._path + "groups" + name
        if path not in self._reg:
            raise KeyError(path)
        return _Group(self._ds, path)

    def __iter__(self):
        return _Iterator(self)

