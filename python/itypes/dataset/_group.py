#!/usr/bin/env python3

from ._item import _Item


class _Iterator:
    def __init__(self, group):
        self._group = group
        self._items = group.item_names()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._items):
            raise StopIteration

        value = self._group[self._items[self._index]]
        self._index += 1
        return value


class _Group:
    def __init__(self, ds, path, title=None):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        if title is not None:
            self._reg[self._path + "title"] = title
        self._new_item_counter = 0

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return self

    def name(self):
        return self._path[-1]

    def title(self):
        path = self._path + "title"
        if path in self._reg:
            return self._reg[path]
        return None

    def item_names(self):
        path = self._path + "items"
        return list(self._reg[path].keys())

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

    def __getitem__(self, name):
        path = self._path + "items" + name
        if path not in self._reg:
            raise KeyError(path)
        return _Item(self._ds, path)

    def __iter__(self):
        return _Iterator(self)