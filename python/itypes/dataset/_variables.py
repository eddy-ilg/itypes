#!/usr/bin/env python3

from ..registry import RegistryPath
from ._variable import _Variable


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

    def remove(self, name):
        self._reg.remove(self._path + name)

    def new(self, name, type):
        self.remove(name)
        d = {
            "type": type
        }
        self._reg[self._path + name] = d
