#!/usr/bin/env python3

from itypes import File
from ._value import _Value


class _Iterator:
    def __init__(self, var):
        self._var = var
        self._groups = var.group_names()
        self._items = None
        if len(self._groups) > 0:
            self._items = var.item_names(self._groups[0])
        self._group_index = 0
        self._item_index = 0

    def __next__(self):
        if self._group_index >= len(self._groups):
            raise StopIteration

        if self._item_index >= len(self._items):
            self._group_index += 1
            if self._group_index >= len(self._groups):
                raise StopIteration
            self._item_index = 0
            self._items = self._var.item_names(self._groups[self._group_index])

        group_name = self._groups[self._group_index]
        item_name = self._items[self._item_index]

        value = self._var[group_name, item_name]
        self._item_index += 1
        return value


class _Variable:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def __getitem__(self, index):
        group_name, item_name = index

        path = self._path + "values" + group_name + item_name
        return _Value(self._ds, path)

    def __contains__(self, index):
        group_name, item_name = index

        path = self._path + "values" + group_name + item_name
        return path in self._reg

    def __iter__(self):
        return _Iterator(self)

    def group_names(self):
        path = self._path + "values"
        if path not in self._reg:
            return []
        return list(self._reg[path].keys())

    def item_names(self, group_name):
        path = self._path + "values" + group_name
        if path not in self._reg:
            raise KeyError(path)
        return list(self._reg[path].keys())

    def name(self):
        return self._path[-1]

    def type(self):
        path = self._path + "type"
        if path not in self._reg:
            return None
        return self._reg[path]

    def extension(self):
        raise NotImplementedError

    def read(self, file, **kwargs):
        if file is None:
            return None
        file = File(file)
        return file.read(**kwargs)

    def write(self, file, data, **kwargs):
        if file is None:
            raise Exception(f"write() needs a file")
        file = File(file)
        file.write(data, **kwargs)
        return self
