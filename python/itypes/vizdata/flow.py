#!/usr/bin/env python3

from ._persistent import _Persistent
from ._persistent_props import _PersistentProperties


class FlowVisualizationData:
    def __init__(self, flow, props=None, label_mask=None):
        self._flow = _Persistent(flow)
        self._props = _PersistentProperties(props)
        self._label_mask = _Persistent(label_mask, dims="hwc")

    def float(self):
        return self._float

    def flow(self):
        return self._flow

    def label_mask(self):
        return self._label_mask

    def reload(self):
        self._flow.reload()
        self._props.reload()
        self._label_mask.reload()