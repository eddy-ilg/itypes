#!/usr/bin/env python3

from ._file_variable import _FileVariable
from .registry import register_variable

class _FloatVariable(_FileVariable):
    def extension(self): return "npz"

register_variable("float", _FloatVariable)