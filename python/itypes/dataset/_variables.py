#!/usr/bin/env python3

from ..json_registry import RegistryPath
from .variables import _instantiate_variable


class _Iterator:
    def __init__(self, variables):
        self._variables = variables
        self._ids = variables.ids()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._ids):
            raise StopIteration

        value = self._variables[self._ids[self._index]]
        self._index += 1
        return value


class _Variables:
    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("variables")

    def __contains__(self, id):
        return self._path.append(id) in self._reg

    def __getitem__(self, id):
        path = self._path + id
        if path not in self._reg:
            raise Exception(f"Variable at path \"{path}\" does not exist")
        type = self._reg[self._path + id + "type"]
        return _instantiate_variable(type, self._ds, path)

    def __delitem__(self, id):
        self.remove(id)
        self._ds._do_auto_write()

    def __iter__(self):
        return _Iterator(self)

    def ids(self):
        path = self._path
        if path not in self._reg:
            return []
        return list(self._reg[path].keys())

    def remove(self, id):
        for viz in self._ds.viz:
            if id in viz.variable_ids():
                del self._ds.viz[viz.id()]
        self._reg.remove(self._path + id)

    def create(self, type, id):
        path = self._path + id
        if path in self._reg:
            self._reg.remove(self._path + id)
        d = {
            "type": type
        }
        self._reg[self._path + id] = d
        return self[id]

    def __str__(self):
        return self.str()

    def str(self, prefix=""):
        str = ""
        for var in self:
            str += var.str(prefix)
        return str

    def __setitem__(self, id, var):
        var = self.create(var.type(), var.id())
        var.copy_from(var, indexing="linear", mode="ref")

    def copy_from(self, other, indexing="linear", mode="ref"):
        for other_var in other:
            var = self.create(other_var.type(), other_var.id())
            var.copy_from(other_var, indexing=indexing, mode=mode)
