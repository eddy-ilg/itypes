#!/usr/bin/env python3

from .registry import register_visualization
from ...vizdata import ImageVisualizationData
from ._single_variable import _SingleVariableVisualization


class _ImageVisualization(_SingleVariableVisualization):
    def data(self, group_name, item_name):
        if self._path + "var" not in self._reg:
            return ImageVisualizationData(None)
        variable_name = self._get("var")
        if (group_name, item_name) not in self._ds.var[variable_name]:
            return ImageVisualizationData(None)
        value = self._ds.var[variable_name][group_name, item_name]
        file = value.file()

        return ImageVisualizationData(file)

    def create_pixviz(self):
        from iviz.renderers import ImagePixmapVisualization
        return ImagePixmapVisualization()

    def create_display(self, manager):
        from iviz.widgets.displays import ImageDisplay
        return ImageDisplay(
            manager,
            self.create_pixviz(),
            id=self._id,
            label=self._get("label")
        )

register_visualization("image", _ImageVisualization)
