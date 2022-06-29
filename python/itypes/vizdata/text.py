#!/usr/bin/env python3

from ._persistent import _Persistent


class TextVisualizationData:
    def __init__(self, text, var_id=None):
        self._text = _Persistent(data=text)
        self._var_id = var_id

    def var_id(self):
        return self._var_id

    def text(self):
        return self._text

    def reload(self):
        self._text.reload()
