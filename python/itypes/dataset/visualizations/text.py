#!/usr/bin/env python3

from .registry import register_visualization
from ...vizdata import TextVisualizationData
from ._single_variable import _SingleVariableVisualization


class _TextVisualization(_SingleVariableVisualization):
    def create(self, type, index, var=None, id=None, colspan=None, rowspan=None, text=None):
        super().create(type, var, index, id, colspan, rowspan)

        if text is not None:
            self._reg[self._path + "text"] = text

    def data(self, group_name, item_name):
        if self._path + "var" not in self._reg:
            return None
        variable_name = self._reg[self._path + "var"]
        if (group_name, item_name) not in self._ds.var[variable_name]:
            return None
        value = self._ds.var[variable_name][group_name, item_name]
        file = value.file()

        return TextVisualizationData(file)

    def create_renderer(self):
        from iviz.pixvizs import TextVisualizationRenderer
        return TextVisualizationRenderer()

    def create_display(self, manager):
        from iviz.widgets.displays import TextDisplay
        return TextDisplay(manager, self.create_renderer(), id=self._id)


register_visualization("text", _TextVisualization)
