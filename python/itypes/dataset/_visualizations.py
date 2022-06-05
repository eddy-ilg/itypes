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
            kwargs['index'] = self._current_col, self._row_idx
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

        def add_cell(self, type, variable, **kwargs):
            kwargs['index'] = self._col_idx, self._current_row
            viz = _instantiate_visualization(
                self._visualizations._ds,
                self._visualizations._path,
                type,
                **kwargs
            )
            self._current_row += 1
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

    def __contains__(self, id):
        if is_list(id):
            return id in self.indices()
        else:
            return self._path + id in self._reg

    def __getitem__(self, id):
        if is_list(id):
            for key, value in self._reg[self._path].items():
                if value['index'] == id:
                    return _reinstantiate_visualization(
                        self._ds,
                        self._path + key,
                     )
            raise Exception(f"visualization \"{id} not found")
        else:
            return _reinstantiate_visualization(
                self._ds,
                self._path + id,
            )

    def __delitem__(self, id):
        self.remove(id)

    def __setitem__(self, key, value):
        # FIXME
        self.set(key, value)

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
