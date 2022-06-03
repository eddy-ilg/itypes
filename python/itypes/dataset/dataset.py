#!/usr/bin/env python3

from ._sequence import _Sequence
from ._variables import _Variables
from ._visualizations import _Visualizations
from ..registry import Registry, RegistryPath
from ..filesystem import File


class Dataset:
    def __init__(self, file=None, abs_paths=False, auto_write=True):
        self._reg = Registry(file)
        self._abs_paths = abs_paths
        self._auto_write = auto_write
        self.viz = _Visualizations(self)
        self.var = _Variables(self)
        self.seq = _Sequence(self)
        self._file = File(file) if file is not None else None

    def base_path(self):
        if self._file is None:
            return None
        return self._file.path()

    def to_dict(self):
        return self._reg.to_dict()

    def write(self, file=None):
        if file is None:
            file = self._file
        self._reg.write(file)
        self._file = file

