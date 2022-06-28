#!/usr/bin/env python3

from .registry import register_visualization
from ...vizdata import FlowVisualizationData
from ._single_variable import _SingleVariableVisualization


class _FlowVisualization(_SingleVariableVisualization):
    DataClass = FlowVisualizationData

    def create_pixviz(self):
        from iviz.renderers import FlowPixmapVisualization
        return FlowPixmapVisualization()

    def create_display(self, manager):
        from iviz.widgets.displays import FlowDisplay
        return FlowDisplay(
            manager,
            self.create_pixviz(),
            id=self._id,
            label=self._get("label")
        )


register_visualization("flow", _FlowVisualization)
