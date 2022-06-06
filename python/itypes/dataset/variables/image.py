#!/usr/bin/env python3

from .._variable import _Variable
from .registry import register_variable


class _ImageVariable(_Variable):
    def extension(self): return "png"

register_variable("image", _ImageVariable)