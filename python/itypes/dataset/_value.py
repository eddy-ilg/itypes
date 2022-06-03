#!/usr/bin/env python3

from ..filesystem import File


class _Value:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def set_ref(self, file, rel_to="cwd", check_if_exists=True):
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