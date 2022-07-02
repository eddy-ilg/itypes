#!/usr/bin/env python3

from ._file_variable import _FileVariable
from .registry import register_variable

class _TextVariable(_FileVariable):
    def extension(self): return "html"

register_variable("text", _TextVariable)