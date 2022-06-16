#!/usr/bin/env python3

from ._persistent import _Persistent


class FlowVisualizationData:
    def __init__(self, flow, annotations=None, label_mask=None):
        self._flow = _Persistent(flow, dims="hwc")
        self._annotations = _Persistent(annotations)
        self._label_mask = _Persistent(label_mask, dims="hwc")

    def flow(self):
        return self._flow

    def annotations(self):
        return self._annotations

    def label_mask(self):
        return self._label_mask

    def reload(self):
        self._flow.reload()
        self._annotations.reload()
        self._label_mask.reload()