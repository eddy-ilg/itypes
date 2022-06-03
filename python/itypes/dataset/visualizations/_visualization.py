#!/usr/bin/env python3

from copy import copy


class _Visualization:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def type(self):
        return self._reg[self._path + "type"]

    def init(self, colspan=None, rowspan=None):
        if colspan is not None:
            self._reg[self._path + "colspan"] = colspan
        if rowspan is not None:
            self._reg[self._path + "rowspan"] = rowspan
