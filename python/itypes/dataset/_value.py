#!/usr/bin/env python3

from ..filesystem import File


class _Value:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def set_ref(self, file, rel_to="cwd", check_if_exists=False):
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

    def file(self):
        path = self._ds.base_path()
        file = File(self._reg[self._path + "path"])
        path = path.cd(file.path())
        return path.file(file.name())

    def data(self, dims="hcw", device="numpy", dtype=None):
        return self.file().read(dims=dims, dtype=dtype, device=device)
