#!/usr/bin/env python3

from ._visualization import _Visualization


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
        self._reg[self._path + "variable"] = var
        self._reg[self._path + "index"] = index

        if var not in self._ds.var:
            self._ds.var.new(var, self.type())

    def _base_id(self):
        return self._reg[self._path + "variable"]

    def variable_names(self):
        return [self._reg[self._path + "variable"]]

