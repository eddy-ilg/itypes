#!/usr/bin/env python3

from copy import copy


class _Visualization:
    def __init__(self, ds, base_path=None, path=None):
        self._ds = ds
        self._reg = ds._reg
        self._base_path = base_path
        self._path = path
        self._id = path[-1] if path is not None else None

    def id(self):
        return self._id

    def type(self):
        return self._reg[self._path + "type"]

    def create(self, colspan=None, rowspan=None):
        if colspan is not None:
            self._reg[self._path + "colspan"] = colspan
        if rowspan is not None:
            self._reg[self._path + "rowspan"] = rowspan

    def index(self):
        return self._reg[self._path + "index"]

    def _base_id(self):
        raise NotImplementedError

