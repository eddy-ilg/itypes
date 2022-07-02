#!/usr/bin/env python3

from ._file_variable import _FileVariable
from .registry import register_variable

class _PropertiesVariable(_FileVariable):
    def extension(self): return "json"

register_variable("props", _PropertiesVariable)