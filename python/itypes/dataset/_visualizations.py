#!/usr/bin/env python3

from ..json_registry import RegistryPath
from .visualizations.registry import _instantiate_visualization, _reinstantiate_visualization
from ..type import is_list


class _Iterator:
    def __init__(self, viz):
        self._viz = viz
        self._indices = viz.indices()
        self._index = 0

    def __next__(self):
        if self._index >= len(self._indices):
            raise StopIteration

        value = self._viz[self._indices[self._index]]
        self._index += 1
        return value
    

class _Visualizations:
    class _Row:
        def __init__(self, visualizations, row_idx):
            self._visualizations = visualizations
            self._row_idx = row_idx
            self._current_col = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, tb):
            if exc_type is None:
                return self

        def skip_cell(self):
            idx = self._current_col, self._row_idx
            if idx in self._visualizations:
                self._visualizations.remove(idx)
            self._current_col += 1
            return self

        def add_cell(self, type, **kwargs):
            index = self._current_col, self._row_idx
            kwargs['index'] = index
            viz = _instantiate_visualization(
                self._visualizations._ds,
                self._visualizations._path,
                type,
                **kwargs
            )
            self._current_col += 1
            return viz

    class _Column:
        def __init__(self, visualizations, col_idx):
            self._visualizations = visualizations
            self._col_idx = col_idx
            self._current_row = 0

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_value, tb):
            if exc_type is None:
                return self

        def skip_cell(self):
            idx = self._col_idx, self._current_row
            if idx in self._visualizations:
                self._visualizations.remove(idx)
            self._current_row += 1
            return self

        def add_cell(self, type, **kwargs):
            index = self._col_idx, self._current_row
            kwargs['index'] = index
            viz = _instantiate_visualization(
                self._visualizations._ds,
                self._visualizations._path,
                type,
                **kwargs
            )
            self._current_col += 1
            return viz

    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("visualizations")
        self._current_col = 0
        self._current_row = 0

    def new_row(self):
        row = self._Row(self, self._current_row)
        self._current_row += 1
        return row

    def new_col(self):
        col = self._Column(self, self._current_col)
        self._current_col += 1
        return col

    def create(self, type, index, **kwargs):
        kwargs['index'] = index
        viz = _instantiate_visualization(
            self._ds,
            self._path,
            type,
            **kwargs
        )
        self._ds._do_auto_write()
        return viz

    def merge_in(self, other, mode=None, **kwargs):
        params = other.params()
        params.update(kwargs)
        viz = _instantiate_visualization(
            self._ds,
            self._path,
            **params
        )
        if mode is not None:
            for new_id, old_id in zip(viz.variable_ids(), other.variable_ids()):
                new_var = self._ds.var[new_id]
                old_var = self._ds.var[old_id]
                self._ds.var.create(type=old_var.id(), id=new_id)
                new_var.copy_from(old_var, mode=mode)

    def indices(self):
        path = self._path
        if path not in self._reg:
            return []
        indices = []
        for value in list(self._reg[path].values()):
            indices.append(value['index'])
        return indices

    def _new_id(self, base_id):
        path = self._path
        if path not in self._reg:
            return base_id
        idx = 1
        id = base_id
        id_path = path + base_id
        while id_path in self._reg:
            id = "%s-%d" % (base_id, idx)
            id_path = path + id
            idx += 1
        return id

    def ids(self):
        path = self._path
        if path not in self._reg:
            return []
        return list(self._reg[path].keys())

    def __contains__(self, id):
        if is_list(id):
            return id in self.indices()
        else:
            return self._path + id in self._reg

    def __getitem__(self, id):
        if is_list(id):
            if self._path not in self._reg:
                raise Exception(f"visualization \"{id}\" not found")
            for key, value in self._reg[self._path].items():
                if value['index'] == id:
                    return _reinstantiate_visualization(
                        self._ds,
                        self._path + key,
                     )
            raise Exception(f"visualization \"{id}\" not found")
        else:
            return _reinstantiate_visualization(
                self._ds,
                self._path + id,
            )

    def __delitem__(self, id):
        self.remove(id)
        self._ds._do_auto_write()

    def __iter__(self):
        return _Iterator(self)

    def remove(self, id):
        if is_list(id):
            for key, value in self._reg[self._path].items():
                if value['index'] == id:
                    self._reg.remove(self._path + key)
            raise Exception(f"visualization \"{id} not found")
        else:
            self._reg.remove(self._path + id)

    def __str__(self):
        return self.str()

    def str(self, prefix=""):
        str = ""
        for viz in self:
            str += viz.str(prefix) + "\n"
        return str

    def __setitem__(self, id, viz):
        params = viz.params()
        self.create(**params, id=id)

    def copy_from(self, other):
        for other_viz in other:
            self.create(**other_viz.params(), id=other_viz.id())
