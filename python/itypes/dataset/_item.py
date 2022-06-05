#!/usr/bin/env python3


class _Item:
    def __init__(self, ds, path, label=None):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        self._item_name = self._path[-1]
        self._group_name = self._path[-3]
        self._group_label = self._reg[self._path + ".." + ".." + "label"]

        exists = self._path in self._reg
        if not exists:
            self._ds.seq._append_item(self._group_name, self._item_name, self._group_label, label)

        if label is not None:
            self._reg[self._path + "label"] = label

    def name(self):
        return self._item_name

    def group_name(self):
        return self._group_name

    def group_label(self):
        return self._group_label

    def label(self):
        path = self._path + "label"
        if path in self._reg:
            return self._reg[path]
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return self

    def __getitem__(self, variable_name):
        if variable_name not in self._ds.var:
            raise Exception(f"\"{variable_name}\" is not an existing variable")
        return self._ds.var[variable_name][self._group_name, self._item_name]

    def set_struct(self, struct):
        for variable in struct.keys():
            if variable not in self._ds.var:
                continue
            self[variable].set_data(struct[variable], dims=struct.dims)
        return self