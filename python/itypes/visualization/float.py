#!/usr/bin/env python3

from ._persistent import _Persistent


class FloatVisualizationData:
    def __init__(self, float, annotations=None, label_mask=None):
        self._float = _Persistent(float)
        self._annotations = _Persistent(annotations)
        self._label_mask = _Persistent(label_mask, dims="hwc")

    def float(self):
        return self._float

    def annotations(self):
        return self._annotations

    def label_mask(self):
        return self._label_mask

    def reload(self):
        self._float.reload()
        self._annotations.reload()
        self._label_mask.reload()