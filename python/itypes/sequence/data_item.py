#!/usr/bin/env python3

import logging
from ..filesystem import Path
from ..type import is_function
from ..conversion import convert_dims, convert_dtype, convert_device

log = logging.getLogger('data_item')


class DataItem:
    def __init__(self, index, rel_file=None, data=None, head="memory", dims=None, base_path=None):
        self._index = index
        self._rel_file = rel_file
        if is_function(data):
            self._generator = data
            self._data = None
        else:
            self._generator = None
            self._data = data
        self._head = head
        self._dims = dims
        self._base_path = base_path

    def _update_data(self):
        if self._generator is not None and self._data is None:
            self._data = self._generator(self._index)
            log.debug(f"Generated data for {self._index} with shape {self._data.shape} and dtype {self._data.dtype}")

    def write_sync(self, keep_memory=False):
        if self._head == "memory" and (self._data is not None or self._generator is not None):
            if self._rel_file is None:
                raise Exception("Tried to synchronize a file to disk that does not have a filename")

            if self._base_path is None:
                raise Exception("Tried to synchronize a file to disk that does not have a base path")

            self._update_data()

            log.debug(f"Syncing {self.file()} to disk")
            self.file().write(self._data, dims=self._dims)
            self._head = "disk"

            if keep_memory is False:
                self._data = None
                self._head = "synced"

    def read_sync(self, dims, dtype=None, device='numpy', keep_memory=False):
        if self._head == "memory" or self._head == "synced":
            self._update_data()
            data = convert_dims(self._data, self._dims, dims)
            data = convert_dtype(data, dtype)
            data = convert_device(data, device)
            if keep_memory:
                self._data = data
                self._dims = dims
                self._newest = "synced"
            return data
        elif self._head == "disk":
            if self._rel_file is None:
                raise Exception("No data or file available for read_sync()")
            log.debug(f"Syncing {self.file()} to memory")
            data = self.file().read(dims=dims, dtype=dtype, device=device)
            if keep_memory:
                self._data = data
                self._dims = dims
                self._head = "synced"
            return data
        else:
            raise Exception("Invalid state encountered")

    def set_base_path(self, path):
        self._base_path = path

    def file(self):
        if self._rel_file is None:
            return None

        if self._base_path is None:
            return self._rel_file
        else:
            return Path(self._base_path + self._rel_file.path()).abs().file(self._rel_file.name())
