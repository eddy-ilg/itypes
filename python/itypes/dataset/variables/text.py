#!/usr/bin/env python3

from ._variable import _Variable
from .registry import register_variable

class _TextVariable(_Variable):
    def extension(self): return "html"

register_variable("text", _TextVariable)