#!/usr/bin/env python3

from .registry import register_visualization
from ...visualization import FlowVisualizationData
from ._single_variable import _SingleVariableVisualization


class _FlowVisualization(_SingleVariableVisualization):
    def data(self, group_name, item_name):
        variable_name = self._reg[self._path + "variable"]
        value = self._ds.var[variable_name][group_name, item_name]
        file = value.file()

        return FlowVisualizationData(file)

    def create_renderer(self):
        from iviz.visualization_renderers import FlowVisualizationRenderer
        return FlowVisualizationRenderer()

    def create_display(self, manager):
        from iviz.widgets.displays import FlowDisplay
        return FlowDisplay(manager, self.create_renderer(), id=self._id)


register_visualization("flow", _FlowVisualization)
