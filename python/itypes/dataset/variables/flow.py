#!/usr/bin/env python3

from .._variable import _Variable
from .registry import register_variable


class _FlowVariable(_Variable):
    def extension(self): return "flo"

register_variable("flow", _FlowVariable)