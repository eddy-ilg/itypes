#!/usr/bin/env python3

from copy import copy
from ...utils import align_tabs


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

    def _str(self, prefix="", indent="  "):
        return prefix + f"{self.id()+':'}\ttype={self.type()}\tindex={tuple(self.index())}\tvars=[{','.join(self.variable_ids())}]"

    def str(self, prefix="", indent="  "):
        return align_tabs(self._str(prefix, indent))

    def __str__(self):
        return self.str()