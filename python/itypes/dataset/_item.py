#!/usr/bin/env python3


class _Item:
    def __init__(self, ds, path, title=None):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        exists = True
        if self._path not in self._reg:
            exists = False

        if title is not None:
            self._reg[self._path + "title"] = title

    def name(self):
        return self._path[-1]

    def title(self):
        path = self._path + "title"
        if path in self._reg:
            return self._reg[path]
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return self

    def __getitem__(self, name):
        item_name = self._path[-1]
        group_name = self._path[-3]
        variables = self._ds.var
        if name not in variables:
            raise Exception(f"\"{name}\" is not an existing variable")
        return variables[name][group_name, item_name]
