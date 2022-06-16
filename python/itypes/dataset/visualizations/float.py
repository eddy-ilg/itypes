#!/usr/bin/env python3

from .registry import register_visualization
from ...visualization import FloatVisualizationData
from ._single_variable import _SingleVariableVisualization


class _FloatVisualization(_SingleVariableVisualization):
    def data(self, group_name, item_name):
        variable_name = self._reg[self._path + "var"]
        value = self._ds.var[variable_name][group_name, item_name]
        file = value.file()

        return FloatVisualizationData(file)

    def create_renderer(self):
        from iviz.visualization_renderers import FloatVisualizationRenderer
        return FloatVisualizationRenderer()

    def create_display(self, manager):
        from iviz.widgets.displays import FloatDisplay
        return FloatDisplay(manager, self.create_renderer(), id=self._id)


register_visualization("float", _FloatVisualization)
