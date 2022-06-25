#!/usr/bin/env python3

import os
from ._sequence import _Sequence
from ._variables import _Variables
from ._visualizations import _Visualizations
from ..json_registry import JsonRegistry, RegistryPath
from ..filesystem import File, Path
from ..utils import align_tabs


class _Iterator:
    def __init__(self, ds):
        self._ds = ds
        self._indices = self._ds.seq.full_item_list()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._indices):
            raise StopIteration

        item = self._indices[self._index]
        item_id = item["item_id"]
        group_id = item["group_id"]
        value = self._ds.seq[group_id][item_id]
        self._index += 1
        return value


class Dataset:
    def __init__(self,
                 file=None,
                 abs_paths=False,
                 auto_write=False,
                 structured_output=True,
                 single_item=False,
                 linear_format="%08d-{var}"):

        self._reg = JsonRegistry(file)
        self._abs_paths = abs_paths
        self._auto_write = auto_write
        self._structured_output = structured_output
        self._linear_format = linear_format
        self._single_item = single_item
        self.viz = _Visualizations(self)
        self.var = _Variables(self)
        self.seq = _Sequence(self)
        self._file = File(file) if file is not None else None

        self._single_item = single_item
        if single_item:
            self._stuctured_output = False
            self._linear_format = "{var}"
            self._single_item_value = self.seq.group().item()

    def _do_auto_write(self):
        if self._auto_write:
            self.write()

    def base_path(self):
        if self._file is None:
            return None
        return self._file.path()

    def to_dict(self):
        return self._reg.to_dict()

    def _make_file(self, file):
        if Path(file.str()).is_dir():
            config_file = Path(file.str()).file('data.gridseq')
            if config_file.exists():
                return config_file
            config_file = Path(file.str()).file('data.json')
            return config_file
        return File(file)

    def write(self, file=None):
        if file is None:
            file = self._file
        file = self._make_file(file)
        self._reg.write(file)
        self._file = file
        return self

    def read(self, file=None):
        if file is None:
            file = self._file
        file = self._make_file(file)

        if file.extension() == "gridseq":
            from ._legacy import read_gridseq
            read_gridseq(self, file)
            return self

        self._reg.read(file)
        self._file = file
        return self

    def __len__(self):
        return len(self.seq.full_item_list())

    def __delitem__(self, index):
        item = self.seq.full_item_list()[index]
        item_id = item["item_id"]
        group_id = item["group_id"]
        del self.seq[group_id][item_id]
        self._do_auto_write()

    def __getitem__(self, index):
        item = self.seq.full_item_list()[index]
        item_id = item["item_id"]
        group_id = item["group_id"]
        return self.seq[group_id][item_id]

    def __iter__(self):
        return _Iterator(self)

    def __str__(self):
        return self.str()

    def str(self, prefix="", indent="  "):
        return align_tabs(self._str(prefix, indent))

    def _str(self, prefix="", indent="  "):
        str = ""
        str += prefix + "variables:\n"
        if len(self.var.ids()) == 0:
            str += prefix + "  (none)\n"
        else:
            str += self.var._str(prefix=prefix + indent, indent=indent)
        str += prefix + "visualizations:\n"
        if len(self.viz.ids()) == 0:
            str += prefix + "  (none)\n"
        else:
            str += self.viz._str(prefix=prefix + indent, indent=indent)
        str += prefix + "sequence:\n"
        if len(self) == 0:
            str += prefix + "  (none)\n"
        else:
            str += self.seq._str(prefix=prefix + indent, indent=indent)
        return str

    def copy_from(self, other, mode="ref"):
        self.viz.copy_from(other.viz)
        self.seq.copy_from(other.seq)
        self.var.copy_from(other.var, mode=mode)
