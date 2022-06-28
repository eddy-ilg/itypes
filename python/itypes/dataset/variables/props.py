#!/usr/bin/env python3

from ._variable import _Variable
from .registry import register_variable

class _PropertiesVariable(_Variable):
    def extension(self): return "json"

register_variable("props", _PropertiesVariable)