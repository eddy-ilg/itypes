#!/usr/bin/env python3

from ._visualization import _Visualization
from copy import deepcopy


class _SingleVariableVisualization(_Visualization):
    def create(self, type, var, index, id=None, colspan=None, rowspan=None, label=None, props=None):
        if id is None:
            id = var
        if id is None:
            id = type
        self._id = self._ds.viz._new_id(id)
        self._path = self._base_path + self._id

        super().create(colspan, rowspan)

        self._reg[self._path + "type"] = type
        if var is not None: self._set("var", var)
        if props is not None: self._set("props", props)
        if label is not None: self._set("label", label)
        self._set("index", index)

        if var not in self._ds.var:
            self._ds.var.create(self.type(), var)

        if props is not None and props not in self._ds.var:
            self._ds.var.create("props", props)

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

    def data(self, group_name, item_name):
        if self._path + "var" not in self._reg:
            return None
        variable_name = self._get("var")
        if (group_name, item_name) not in self._ds.var[variable_name]:
            return None
        value = self._ds.var[variable_name][group_name, item_name]
        file = value.file()

        props_file = None
        if self._path + "props" in self._reg:
            variable_name = self._get("props")
            if (group_name, item_name) in self._ds.var[variable_name]:
                value = self._ds.var[variable_name][group_name, item_name]
                props_file = value.file()

        return self.DataClass(file, props_file)