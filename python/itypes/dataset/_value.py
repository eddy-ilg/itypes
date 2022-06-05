#!/usr/bin/env python3

from ..filesystem import File


class _Value:
    def __init__(self, ds, path):
        self._ds = ds
        self._reg = ds._reg
        self._path = path

    def variable_name(self):
        path = self._path + ".." + ".." + ".."
        return str(path[-1])

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

    def set_data(self, data, extension=None, dims="hwc"):
        if data is None:
            self._reg.remove(self._path + "path")
            return

        if extension is None:
            extension = self._scene._data._seq.grid[id].extension()

        if self._scene._data._seq.structured_output():
            file = Path(self._scene.name()).cd(self.name()).file(f"{id}.{extension}")
        else:
            linear_format = self._scene._data._seq.linear_format()
            if "{id}" not in linear_format:
                raise Exception("linear_format needs to contain '{id}'")
            filename = (linear_format % self._linear_index.value()).replace("{id}", id) + '.' + extension
            file = File(filename)

        log.debug(f"Setting data for frame_name='{self._name}', id='{id}' pointing to '{file}'")
        index = DataIndex(
            id=id,
            scene=self._scene.name(),
            frame=self._name,
            linear_index=self._linear_index
        )
        self[id] = DataItem(
            index,
            data=data,
            rel_file=file,
            head="memory",
            dims=dims
        )

        if self._scene._data._seq.write_write_sync():
            path = self._scene._data._seq.path()
            if path is None:
                raise Exception("Synchronized writes require a sequence with filename=... to be able to determine the base path")
            self[id].set_base_path(path)
            self[id].write_sync()

        return self

    def file(self):
        path = self._ds.base_path()
        if self._path + "path" not in self._reg:
            return None
        file = File(self._reg[self._path + "path"])
        path = path.cd(file.path())
        return path.file(file.name())

    def data(self, dims="hcw", device="numpy", dtype=None):
        file = self.file()
        if file is None:
            return None
        return file.read(dims=dims, dtype=dtype, device=device)
