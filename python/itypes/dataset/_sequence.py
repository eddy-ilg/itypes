#!/usr/bin/env python3

from ._group import _Group
from ..json_registry import RegistryPath


class _Iterator:
    def __init__(self, seq):
        self._seq = seq
        self._groups = seq.group_names()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._groups):
            raise StopIteration

        value = self._seq[self._groups[self._index]]
        self._index += 1
        return value


class _Sequence:
    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("sequence")

    def group(self, name="default", label=None):
        if label is None:
            label = name
        if name == "default" and label is not None:
            name = label
        path = self._path + "groups" + name
        return _Group(self._ds, path, label)

    def group_names(self):
        path = self._path + "groups"
        return list(self._reg[path].keys())

    def item_names(self, group_name):
        path = self._path + "groups" + group_name + "items"
        if path not in self._reg:
            raise KeyError(path)
        return list(self._reg[path].keys())

    def _current_new_index(self):
        path = self._path + "item_list"
        if path not in self._reg:
            return 0
        list = self._reg[path]
        return len(list)

    def _append_group(self, group_name, label):
        path = self._path + "group_list"
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": self._current_new_index(),
            "name": group_name,
            "label": label
        })

    def _append_item(self, group_name, item_name, group_label, label):
        path = self._path + "item_list"
        index = self._current_new_index()
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": index,
            "group_name": group_name,
            "group_label": group_label,
            "item_name": item_name,
            "item_label": label
        })

        path = self._path + "groups" + group_name + "item_list"
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": index,
            "name": item_name,
            "label": label
        })

    def full_item_list(self):
        path = self._path + "item_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def item_list(self, group_name):
        path = self._path + "groups" + group_name + "item_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def group_list(self):
        path = self._path + "group_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def __getitem__(self, name):
        path = self._path + "groups" + name
        if path not in self._reg:
            raise KeyError(path)
        return _Group(self._ds, path)

    def __iter__(self):
        return _Iterator(self)

