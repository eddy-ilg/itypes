#!/usr/bin/env python3

from ._visualization import _Visualization
from .registry import register_visualization


class _FlowVisualization(_Visualization):
    def init(self, variable, colspan=None, rowspan=None):
        super().init(colspan, rowspan)

        self._reg[self._path + "variable"] = variable

        if variable not in self._ds.var:
            self._ds.var.new(variable, self.type())

register_visualization("flow", _FlowVisualization)
