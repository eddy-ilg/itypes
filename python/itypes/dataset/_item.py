#!/usr/bin/env python3


class _Iterator:
    def __init__(self, item):
        self._item = item
        self._names = item.variable_names()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._names):
            raise StopIteration

        value = self._item[self._names[self._index]]
        self._index += 1
        return value


class _Item:
    def __init__(self, ds, path, label=None):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

        self._item_name = self._path[-1]
        self._group_name = self._path[-3]
        self._group_label = self._reg[self._path + ".." + ".." + "label"]

        exists = self._path in self._reg
        if not exists:
            self._ds.seq._append_item(self._group_name, self._item_name, self._group_label, label)

        if label is not None:
            self._reg[self._path + "label"] = label

    def __iter__(self):
        return _Iterator(self)
    
    def name(self):
        return self._item_name

    def group_name(self):
        return self._group_name

    def group_label(self):
        return self._group_label

    def label(self):
        path = self._path + "label"
        if path in self._reg:
            return self._reg[path]
        return None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        if exc_type is None:
            return self

    def variable_names(self):
        names = []
        for variable in self._ds.var:
            if variable.name() in self:
                names.append(variable.name())
        return names

    def __getitem__(self, variable_name):
        if variable_name not in self._ds.var:
            raise Exception(f"\"{variable_name}\" is not an existing variable")
        return self._ds.var[variable_name][self._group_name, self._item_name]

    def __contains__(self, variable_name):
        if variable_name not in self._ds.var:
            return False
        return (self._group_name, self._item_name) in self._ds.var[variable_name]

    def set_struct(self, struct):
        for variable in struct.keys():
            if variable not in self._ds.var:
                continue
            self[variable].set_data(struct[variable], dims=struct.dims)

        if self._ds._auto_write:
            self._ds.write()

        return self

    def numpy_struct(self, dims):
        import numpy as np
        from ..struct import NumpyStruct
        struct = NumpyStruct(dims)
        for variable_name in self:
            struct[variable_name] = self[variable_name].data(dims=dims, dtype=np.float32)
        struct.item_name = self.name()
        struct.group_name = self.group_name()
        return struct

    def torch_struct(self, dims, device):
        import numpy as np
        from ..struct import TorchStruct
        struct = TorchStruct(dims)
        for value in self:
            struct[value.variable_name()] = self[value.variable_name()].data(dims=dims, dtype=np.float32, device=device)
        struct.frame_name = self.name()
        struct.scene_name = self.group_name()
        return struct