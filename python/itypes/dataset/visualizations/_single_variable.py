#!/usr/bin/env python3

from ._visualization import _Visualization
from copy import deepcopy


class _SingleVariableVisualization(_Visualization):
    def create(self, type, var, index, id=None, colspan=None, rowspan=None):
        if id is None:
            id = var
        self._id = self._ds.viz._new_id(id)
        self._path = self._base_path + self._id

        if index in self._ds.viz:
            self._ds.viz.remove(index)

        super().create(colspan, rowspan)

        self._reg[self._path + "type"] = type
        self._reg[self._path + "var"] = var
        self._reg[self._path + "index"] = index

        if var not in self._ds.var:
            self._ds.var.create(self.type(), var)

    def _base_id(self):
        return self._reg[self._path + "var"]

    def params(self):
        if self._path not in self._reg:
            return {}
        return deepcopy(self._reg[self._path])

    def variable_ids(self):
        return [self._reg[self._path + "var"]]

    def __getattr__(self, item):
        if item =="sv":
            return self.single_value()
        return super().__getattr__(self, item)

    def single_value(self):
        var = self._reg[self._path + "var"]
        return self._ds._single_item_value[var]

