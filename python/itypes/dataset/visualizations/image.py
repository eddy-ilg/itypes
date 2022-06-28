#!/usr/bin/env python3

from .registry import register_visualization
from ...vizdata import ImageVisualizationData
from ._single_variable import _SingleVariableVisualization


class _ImageVisualization(_SingleVariableVisualization):
    DataClass = ImageVisualizationData

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
