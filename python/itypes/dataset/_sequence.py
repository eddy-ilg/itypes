#!/usr/bin/env python3

from ._group import _Group
from ..registry import RegistryPath


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