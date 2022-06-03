#!/usr/bin/env python3


class _Item:
    def __init__(self, ds, path, title):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        exists = True
        if self._path not in self._reg:
            exists = False

        self._reg[self._path + "title"] = title

        if not exists and self._ds._auto_write:
            self._ds.write()

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