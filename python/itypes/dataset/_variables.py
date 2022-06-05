#!/usr/bin/env python3

from ..json_registry import RegistryPath
from ._variable import _Variable


class _Iterator:
    def __init__(self, variables):
        self._variables = variables
        self._names = variables.names()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._names):
            raise StopIteration

        value = self._variables[self._names[self._index]]
        self._index += 1
        return value


class _Variables:
    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("variables")

    def __contains__(self, name):
        return self._path.append(name) in self._reg

    def __getitem__(self, name):
        return _Variable(self._ds, self._path + name)

    def __delitem__(self, name):
        self.remove(name)

    def __iter__(self):
        return _Iterator(self)

    def names(self):
        path = self._path
        return list(self._reg[path].keys())

    def remove(self, name):
        self._reg.remove(self._path + name)

    def new(self, name, type):
        self.remove(name)
        d = {
            "type": type
        }
        self._reg[self._path + name] = d

