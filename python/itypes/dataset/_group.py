#!/usr/bin/env python3

from collections import OrderedDict
from ._item import _Item


class _Group:
    def __init__(self, ds, path, title):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        self._reg[self._path + "title"] = title
        self._new_item_counter = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return self

    def _new_name(self):
        name = "%08d" % self._new_item_counter
        self._new_item_counter += 1
        return name

    def item(self, name=None, title=None):
        if name is None:
            name = self._new_name()
        if title is None:
            title = name
        path = self._path + "items" + name
        return _Item(self._ds, path, title)