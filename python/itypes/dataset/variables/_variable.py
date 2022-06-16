#!/usr/bin/env python3

from itypes import File
from .._value import _Value


class _Iterator:
    def __init__(self, var):
        self._var = var
        self._groups = var.group_ids()
        self._items = None
        if len(self._groups) > 0:
            self._items = var.item_ids(self._groups[0])
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
            self._items = self._var.item_ids(self._groups[self._group_index])

        group_id = self._groups[self._group_index]
        item_id = self._items[self._item_index]

        value = self._var[group_id, item_id]
        self._item_index += 1
        return value


class _Variable:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def __getitem__(self, index):
        group_id, item_id = index

        path = self._path + "values" + group_id + item_id
        return _Value(self._ds, path)

    def __contains__(self, index):
        group_id, item_id = index

        path = self._path + "values" + group_id + item_id
        return path in self._reg

    def __iter__(self):
        return _Iterator(self)

    def __setitem__(self, index, value):
        group_id, item_id = index
        self[group_id, item_id].copy_from(value)

    def str(self, prefix=""):
        indent = "  "
        str = ""
        str += prefix + f"{self.id()+':':10s}\ttype={self.type():10s}\n"
        for value in self:
            str += prefix + indent + f"{value.group_id()}/{value.item_id()} -> {value.file()}\n"
        return str

    def __str__(self):
        return self.str()

    def copy_from(self, other, indexing="linear", mode=""):
        if indexing == "linear":
            for i in range(0, len(self._ds)):
                item = self._ds[i]
                group_id = item.group_id()
                item_id = item.id()
                if i < len(other._ds):
                    self[group_id, item_id].copy_from(other._ds[i][other.id()], mode=mode)
        elif indexing == "id":
            for group in self._ds.seq:
                for item in group:
                    group_id = item.group_id()
                    item_id = item.id()
                    if (group_id, item_id) in other:
                        self[group_id, item_id].copy_from(other[group_id, item_id], mode=mode)
        else:
            raise Exception(f"invalid value for indexing= parameter: {indexing}")

    def group_ids(self):
        path = self._path + "values"
        if path not in self._reg:
            return []
        return list(self._reg[path].keys())

    def item_ids(self, group_id):
        path = self._path + "values" + group_id
        if path not in self._reg:
            raise KeyError(path)
        return list(self._reg[path].keys())

    def id(self):
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
