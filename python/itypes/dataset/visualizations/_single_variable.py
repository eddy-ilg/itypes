#!/usr/bin/env python3

from ._visualization import _Visualization
from copy import deepcopy


class _SingleVariableVisualization(_Visualization):
    def create(self, type, var, index, id=None, colspan=None, rowspan=None):
        if id is None:
            id = var
        if id is None:
            id = type
        self._id = self._ds.viz._new_id(id)
        self._path = self._base_path + self._id

        super().create(colspan, rowspan)

        self._reg[self._path + "type"] = type
        if var is not None: self._set("var", var)
        self._set("index", index)

        if var not in self._ds.var:
            self._ds.var.create(self.type(), var)

    def _base_id(self):
        return self._get("var")

    def params(self):
        if self._path not in self._reg:
            return {}
        return deepcopy(self._reg[self._path])

    def variable_ids(self):
        return [self._get("var")]

    def __getattr__(self, item):
        if item =="sv":
            return self.single_value()
        raise KeyError(item)

    def single_value(self):
        var = self._get("var")
        return self._ds._single_item_value[var]

