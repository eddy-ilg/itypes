#!/usr/bin/env python3

from ..registry import RegistryPath
from .visualizations.registry import _instantiate_visualization


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
            idx = self._current_col, self._row_idx
            viz = _instantiate_visualization(
                self._visualizations._ds,
                self._visualizations._path + idx,
                type
            )
            viz.init(**kwargs)
            self._current_col += 1
            return self

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
            idx = self._col_idx, self._current_row
            viz = _instantiate_visualization(
                self._visualizations._ds,
                self._visualizations._path + idx,
                type
            )
            viz.init(**kwargs)
            self._current_col += 1
            return self

    def __init__(self, ds):
        self._ds = ds
        self._reg = ds._reg
        self._path = RegistryPath("visualization")
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

    def __contains__(self, idx):
        return self._path + idx in self._reg

    def __getitem__(self, idx):
        return self._reg[self._path + idx]

    def __delitem__(self, key):
        self.remove(key)

    def __setitem__(self, key, value):
        self.set(key, value)

    # TODO get indices / iterate

    def remove(self, idx):
        self._reg.remove(self._path + idx)

    # def set(self, idx, visualization):
    #     # if idx in self._data:
    #     #     self.remove(idx)
    #     # visualization._register(self._ds)
    #     # self._data[idx] = visualization
    #     return self

