#!/usr/bin/env python3

from ._sequence import _Sequence
from ._variables import _Variables
from ._visualizations import _Visualizations
from ..json_registry import JsonRegistry, RegistryPath
from ..filesystem import File


class _Iterator:
    def __init__(self, ds):
        self._ds = ds
        self._indices = self._ds.seq.full_item_list()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._indices):
            raise StopIteration

        item = self._indices[self._index]
        item_name = item["item_name"]
        group_name = item["group_name"]
        value = self._ds.seq[group_name][item_name]
        self._index += 1
        return value


class Dataset:
    def __init__(self, file=None, abs_paths=False, auto_write=False):
        self._reg = JsonRegistry(file)
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
        return self

    def read(self, file=None):
        if file is None:
            file = self._file
        self._reg.read(file)
        self._file = file
        self._dirty = True
        return self

    def __len__(self):
        return len(self.seq.full_item_list())

    def __getitem__(self, index):
        item = self.seq.full_item_list()[index]
        item_name = item["item_name"]
        group_name = item["group_name"]
        return self.seq[group_name][item_name]

    def __iter__(self):
        return _Iterator(self)

