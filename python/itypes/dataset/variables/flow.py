#!/usr/bin/env python3

from ._file_variable import _FileVariable
from .registry import register_variable


class _FlowVariable(_FileVariable):
    def extension(self): return "flo"

register_variable("flow", _FlowVariable)