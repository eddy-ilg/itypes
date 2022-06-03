#!/usr/bin/env python3

from ._value import _Value


class _Variable:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def __getitem__(self, index):
        group_name, item_name = index

        path = self._path + "values" + group_name + item_name
        return _Value(self._ds, path)