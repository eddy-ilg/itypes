#!/usr/bin/env python3

from ._group import _Group
from ..json_registry import RegistryPath
from ..utils import align_tabs


class _Iterator:
    def __init__(self, seq):
        self._seq = seq
        self._groups = seq.group_ids()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._groups):
            raise StopIteration

        value = self._seq[self._groups[self._index]]
        self._index += 1
        return value


class _DeferredIndexRebuildContext:
    def __init__(self, seq):
        self._seq = seq

    def __enter__(self):
        self._old_rebuild_index = self._seq._rebuild_index
        self._seq._rebuild_index = False
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self._seq._rebuild_index = self._old_rebuild_index
        if self._seq._needs_index_rebuild:
            self._seq.rebuild_linear_index()
        if exc_type is None:
            return self


class _Sequence:
    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("sequence")

        self._rebuild_index = True
        self._needs_index_rebuild = False

    def deferred_index_rebuild(self):
        return _DeferredIndexRebuildContext(self)

    def group(self, id="default", label=None):
        if label is None:
            label = id
        if id == "default" and label is not None:
            id = label
        path = self._path + "groups" + id
        return _Group(self._ds, path, label)

    def group_ids(self):
        path = self._path + "groups"
        return list(self._reg[path].keys())

    def item_ids(self, group_id):
        path = self._path + "groups" + group_id + "items"
        if path not in self._reg:
            raise KeyError(path)
        return list(self._reg[path].keys())

    def _current_new_index(self):
        path = self._path + "item_list"
        if path not in self._reg:
            return 0
        list = self._reg[path]
        return len(list)

    def _append_group(self, group_id, label):
        path = self._path + "group_list"
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": self._current_new_index(),
            "id": group_id,
            "label": label
        })

    def _append_item(self, group_id, item_id, group_label, label):
        path = self._path + "item_list"
        index = self._current_new_index()
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": index,
            "group_id": group_id,
            "group_label": group_label,
            "item_id": item_id,
            "item_label": label
        })

        path = self._path + "groups" + group_id + "item_list"
        if path not in self._reg:
            self._reg[path] = []
        self._reg[path].append({
            "index": index,
            "id": item_id,
            "label": label
        })

    def full_item_list(self):
        path = self._path + "item_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def item_list(self, group_id):
        path = self._path + "groups" + group_id + "item_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def group_list(self):
        path = self._path + "group_list"
        if path not in self._reg:
            return []
        return self._reg[path]

    def rebuild_linear_index(self):
        item_list_path  = self._path + "item_list"
        self._reg[item_list_path] = []

        group_list_path = self._path + "group_list"
        self._reg[group_list_path] = []

        for group in self:
            group_item_list_path = group._path + "item_list"
            self._reg[group_item_list_path] = []

        for group in self:
            self._append_group(
                group.id(),
                group.label()
            )
            for item in group:
                self._append_item(
                    group.id(),
                    item.id(),
                    group.label(),
                    item.label()
                )

        self._needs_index_rebuild = False

    def flag_linear_index_as_dirty(self):
        if self._rebuild_index: self.rebuild_linear_index()
        else:                   self._needs_index_rebuild = True

    def remove(self, id, delete_files=False):
        if delete_files:
            raise NotImplementedError

        path = self._path + "groups" + id
        del self._reg[path]

        self.flag_linear_index_as_dirty()

    def __delitem__(self, id):
        self.remove(id)
        self._ds._do_auto_write()

    def __getitem__(self, id):
        path = self._path + "groups" + id
        if path not in self._reg:
            raise KeyError(path)
        return _Group(self._ds, path)

    def __iter__(self):
        return _Iterator(self)

    def __str__(self):
        return self.str()

    def str(self, prefix="", indent="  "):
        return align_tabs(self._str(prefix, indent))

    def _str(self, prefix="", indent="  "):
        str = ""
        index = 0
        for group in self:
            str += group._str(prefix, indent, start_index=index)
            index += len(group.item_ids())
        return str

    def copy_from(self, other):
        for other_group in other:
            new_group = self.group(other_group.id(), other_group.label())
            for other_item in other_group:
                new_item = new_group.item(other_item.id(), other_item.label())

        self._ds._do_auto_write()