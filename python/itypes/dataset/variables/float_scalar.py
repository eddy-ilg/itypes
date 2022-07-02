#!/usr/bin/env python3

from ._variable import _Variable
from .registry import register_variable

class _FloatScalarVariable(_Variable):
    pass

register_variable("float-scalar", _FloatScalarVariable)