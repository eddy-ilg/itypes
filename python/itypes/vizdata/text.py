#!/usr/bin/env python3

from ._persistent import _Persistent


class TextVisualizationData:
    def __init__(self, text):
        self._text = _Persistent(data=text)

    def text(self):
        return self._text

    def reload(self):
        self._text.reload()
