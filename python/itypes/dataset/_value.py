#!/usr/bin/env python3

from itypes import Path
from ..filesystem import File


class _Value:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def variable_name(self):
        path = self._path + ".." + ".." + ".."
        return str(path[-1])

    def variable(self):
        return self._ds.var[self.variable_name()]

    def type(self):
        path = self._path + ".." + ".." + ".." + "type"
        return self._reg[path]

    def group_name(self):
        return str(self._path[-2])

    def item_name(self):
        return str(self._path[-1])

    def set_ref(self, file, rel_to="cwd", check_if_exists=False):
        if file is None:
            self._reg.remove(self._path + "path")

        file = File(file)

        if rel_to == "cwd":
            file = file.abs()
        elif rel_to == "output":
            base_path = self._ds.base_path()
            file = base_path.cd(file.path()).file(file.name()).abs()
        else:
            raise Exception("rel_to must be 'cwd' or 'output'")

        if check_if_exists:
            if not file.exists():
                raise Exception(f"External sequence file '{file}' does not exist")

        if not self._ds._abs_paths:
            file = file.rel_to(self._ds.base_path())

        self._reg[self._path + "path"] = str(file)

        if self._ds._auto_write:
            self._ds.write()

    def set_data(self, data, extension=None, **kwargs):
        if data is None:
            self._reg.remove(self._path + "path")

        variable = self.variable()
        if extension is None:
            extension = variable.extension()

        if self._ds._structured_output:
            file = Path(self.group_name()).cd(self.item_name()).file(f"{self.variable_name()}.{extension}")
        else:
            linear_format = self._ds._linear_format
            linear_index = len(self._ds)
            if "{var}" not in linear_format:
                raise Exception("linear_format needs to contain '{var}'")
            filename = (linear_format % linear_index).replace("{var}", self.variable_name()) + '.' + extension
            file = File(filename)

        abs_file = (self._ds.base_path() + file.path()).abs().file(file.name())
        variable.write(abs_file, data, **kwargs)
        self._reg[self._path + "path"] = str(file) if not self._ds._abs_paths else str(abs_file)

        if self._ds._auto_write:
            self._ds.write()

        return self

    def file(self):
        path = self._ds.base_path()
        if self._path + "path" not in self._reg:
            return None
        file = File(self._reg[self._path + "path"])
        path = path.cd(file.path())
        return path.file(file.name())

    def data(self, **kwargs):
        file = self.file()
        if file is None:
            return None
        file = File(file)
        return self.variable().read(file, **kwargs)
