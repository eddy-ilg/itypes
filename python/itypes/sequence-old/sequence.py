#!/usr/bin/env python3

import numpy as np
import logging
from collections import OrderedDict
from ..filesystem import File
from ..filesystem import Path
from .data_index import _LinearIndex, DataIndex
from .data_item import DataItem
from .io import read_gridseq, write_gridseq, read_json, write_json

log = logging.getLogger('sequence')

_sequence_registry = {}

def singleton_sequence(**kwargs):
    global _sequence_registry

    # Determine filename
    filename = None
    if 'filename' in kwargs:
        filename = kwargs['filename']
    elif 'folder' in kwargs:
        filename = Path(kwargs['folder']).file("data.gridseq")
    if filename is None:
        raise Exception('Error: singleton_sequence requires a filename or path to determine a unique id')
    name = str(filename)

    # Add to registry if it doesn't exist and return sequence
    # with initialized = False
    if name not in _sequence_registry:
        _sequence_registry[name] = Sequence(**kwargs)
        return _sequence_registry[name]

    # Set initialized = True and return existing sequence
    _sequence_registry[name].set_initialized(True)
    return _sequence_registry[name]

class Sequence:
    class Grid(dict):
        class Cell:
            def __init__(self, grid, type, id, config=None, source_seq=None, source_id=None,  title=None, source_method="linear"):
                self._grid = grid
                self._type = type
                self._id = id
                self._config = config
                self._title = title
                self._source_seq = source_seq
                self._source_id = source_id if source_id is not None else id
                if source_method not in ["linear", "structured"]:
                    raise Exception(f"source_method {source_method} is invalid, use either \"linear\" or \"structured\"")
                self._source_method = source_method

            def id(self): return self._id
            def type(self): return self._type
            def title(self): return self._title
            def source_seq(self): return self._source_seq
            def source_id(self): return self._source_id
            def source_method(self): return self._source_method

            def extension(self):
                if self._type == "image": return "png"
                elif self._type == "flow": return "flo"
                elif self._type == "float": return "blob"
                else:
                    raise Exception(f"Don't know a default extension for data type '{self._type}'")

            def set_ext(self, file, rel_to="cwd", check_if_exists=True):
                self._grid._seq.frames()[0].set_ext(self._id, file, rel_to, check_if_exists)

            def set_data(self, data, extension=None, dims="hwc"):
                self._grid._seq.frames()[0].set_data(self._id, data, extension, dims)

        class Row:
            def __init__(self, grid, row_idx):
                self._grid = grid
                self._row_idx = row_idx
                self._current_col = 0

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, tb):
                if exc_type is None:
                    return self

            def skip_cell(self):
                idx = self._current_col, self._row_idx
                log.debug(f"Skipping cell {idx}")
                if idx in self._grid:
                    del self.grid[idx]
                self._current_col += 1
                return self

            def add_cell(self, type, id=None, config=None, **kwargs):
                idx = self._current_col, self._row_idx
                log.debug(f"Adding cell {idx}, type='{type}', id='{id}'")
                cell = self._grid.Cell(self._grid, type, id, config, **kwargs)
                self._grid[idx] = cell
                self._current_col += 1
                return cell

        class Column:
            def __init__(self, grid, col_idx):
                self._grid = grid
                self._col_idx = col_idx
                self._current_row = 0

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, tb):
                if exc_type is None:
                    return self

            def skip_cell(self):
                idx = self._col_idx, self._current_row
                log.debug(f"Skipping cell {idx}")
                if idx in self._grid:
                    del self.grid[idx]
                self._current_row += 1
                return self

            def add_cell(self, type, id, config=None):
                idx = self._col_idx, self._current_row
                log.info(f"Adding cell {idx}, type='{type}', id='{id}'")
                cell = self._grid.Cell(self._grid, type, id, config)
                self._grid[idx] = cell
                self._current_row += 1
                return cell

        def __init__(self, seq):
            super().__init__()
            self._seq = seq
            self._current_col = 0
            self._current_row = 0

        def __getitem__(self, item):
            try:
                return super().__getitem__(item)
            except:
                for pos, cell in self.items():
                    if cell.id() == item:
                        return cell
            raise KeyError()

        def __iter__(self):
            return self.values().__iter__()

        def new_row(self):
            row = self.Row(self, self._current_row)
            self._current_row += 1
            return row

        def new_column(self):
            col = self.Column(self, self._current_col)
            self._current_col += 1
            return col

        def current_col(self):
            return self._current_col

        def current_row(self):
            return self._current_row

        def contains_id(self, id):
            # TODO: this could be optimized by a cache
            # by keeping current ids in a set
            for pos, cell in self.items():
                if cell.id() == id:
                    return True
            return False

    class Data(OrderedDict):
        class Frame(dict):
            def __init__(self, scene, name, linear_index):
                self._scene = scene
                self._name = name
                self._linear_index = linear_index

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, tb):
                if exc_type is None:
                    return self

            def linear_index(self): return self._linear_index
            def name(self): return self._name
            def scene_name(self): return self._scene.name()

            def _check_id(self, id):
                if not self._scene._data._seq.grid.contains_id(id):
                    raise Exception(f"Sequence id '{id}' not found")

            def data(self, id, dims, dtype=None, device='numpy'):
                if id not in self:
                    return None

                return self[id].read_sync(dims, dtype, device)

            def numpy_struct(self, dims):
                from itypes import NumpyStruct
                struct = NumpyStruct(dims)
                for id in self:
                    struct[id] = self.data(id, dims, dtype=np.float32)
                struct.frame_name = self.name()
                struct.scene_name = self._scene.name()
                return struct

            def torch_struct(self, dims, device):
                from itypes import TorchStruct
                struct = TorchStruct(dims)
                for id in self:
                    struct[id] = self.data(id, dims, dtype=np.float32, device=device)
                struct.frame_name = self.name()
                struct.scene_name = self._scene.name()
                return struct

            def fill_from_sources(self):
                grid = self._scene._data._seq.grid
                source_mode = self._scene._data._seq.source_mode()

                for cell in grid:
                    if cell.source_seq() is None:
                        continue

                    source_seq = cell.source_seq()
                    source_id = cell.source_id()
                    source_method = cell.source_method()

                    if source_method == "linear":
                        source_frame = source_seq.frames()[self._linear_index.value()]
                    else:
                        source_frame = source_seq.data[self._scene.name()][self._name]

                    if source_mode == "ref":
                        self.set_ext(cell.id(), source_frame[source_id].file())
                    else:
                        data = source_frame[source_id].read_sync(dims="hwc")
                        log.debug(f"Read source data with shape {data.shape}, dtype {data.dtype}")
                        self.set_data(cell.id(), data)

            def set_ext(self, id, file, rel_to="cwd", check_if_exists=True):
                if not self._scene._data._seq.enabled():
                    return

                self._check_id(id)

                file = File(file)

                if rel_to == "cwd":
                    file = file.abs()
                elif rel_to == "output":
                    base_path = self._scene._data._seq.path()
                    file = base_path.cd(file.path()).file(file.name()).abs()
                else:
                    raise Exception("rel_to must be 'cwd' or 'output'")

                if check_if_exists:
                    if not file.exists():
                        raise Exception(f"External sequence file '{file}' does not exist")

                log.debug(f"Setting external reference for frame_name='{self._name}', id='{id}' to '{file}'")
                index = DataIndex(
                    id=id,
                    scene=self._scene.name(),
                    frame=self._name,
                    linear_index=self._linear_index,
                )
                self[id] = DataItem(
                    index,
                    rel_file=file,
                    head="disk"
                )
                return self

            def set_data(self, id, data, extension=None, dims="hwc"):
                if not self._scene._data._seq.enabled():
                    return

                self._check_id(id)

                if data is None:
                    index = DataIndex(
                        id=id,
                        scene=self._scene.name(),
                        frame=self._name,
                        linear_index=self._linear_index
                    )
                    self[id] = DataItem(
                        index,
                        data=None,
                        rel_file=None,
                        head="memory",
                        dims=dims
                    )
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

            def set_struct(self, struct):
                if not self._scene._data._seq.enabled():
                    return

                for id in struct.keys():
                    if not self._scene._data._seq.grid.contains_id(id):
                        continue
                    self.set_data(id, struct[id], dims=struct.dims)
                return self

        class Scene(OrderedDict):
            def __init__(self, data, name):
                super().__init__()
                self._data = data
                self._name = name
                self._frame_idx = 0

            def __enter__(self):
                return self

            def __exit__(self, exc_type, exc_value, tb):
                if exc_type is None:
                    return self

            def __iter__(self):
                return self.values().__iter__()

            def name(self): return self._name

            def sample(self, name=None):
                if not self._data._seq.enabled():
                    return self._data.Frame(self, None, None)

                if name is None:
                    name = "%010d" % self._frame_idx
                    self._frame_idx += 1
                log.debug(f"Creating frame, name='{name}'")
                linear_index = _LinearIndex()
                frame = self._data.Frame(self, name, linear_index)
                self[name] = frame
                self._data.reindex()
                frame.fill_from_sources()
                return frame

            def add(self, frame):
                self[frame.name()] = frame

        def __iter__(self):
            return self.values().__iter__()

        def __init__(self, seq):
            super().__init__()
            self._seq = seq
            self._scene_idx = 0

        def scene(self, name=None):
            if not self._seq.enabled():
                return self.Scene(self, None)

            if name is None:
                name = "scene-%04d" % self._scene_idx
                self._scene_idx += 1
            log.debug(f"Creating scene, name='{name}'")
            scene = self.Scene(self, name)
            self[name] = scene
            return scene

        def reindex(self):
            # TODO: this could be optimized by a cache
            index = 0
            for scene in self:
                for frame in scene:
                    frame.linear_index().set_value(index)
                    index += 1
            return self

        def total_length(self):
            # TODO: this could be optimized by a cache
            total_length = 0
            for scene in self:
                for frame in scene:
                    total_length += 1
            return total_length

    def __init__(self,
                 filename=None,
                 folder=None,
                 structured_output=True,
                 linear_format="%08d-{id}",
                 write_sync=None,
                 source_mode="copy", single_frame=False, enabled=True):
        # Public variables
        self.data = self.Data(self)
        self.grid = self.Grid(self)

        # Determine filename
        if filename is None and folder is not None:
            filename = Path(folder).file("data.gridseq")

        # Private variables
        self._filename = File(filename) if filename is not None else None
        self._stuctured_output = structured_output
        self._linear_format = linear_format
        self._linear_index = 0
        self._initialized = False
        self._enabled = enabled

        if write_sync is not None:
            self._write_sync = write_sync
        else:
            self._write_sync = self._filename is not None

        if source_mode not in ["copy", "ref"]:
            raise Exception(f"Source mode {source_mode} is invalid, specify either\"copy\" or \"ref\"")
        self._source_mode = source_mode

        self._single_frame = single_frame
        if single_frame:
            self._stuctured_output = False
            self.data.scene("default").sample("default")

    def set_enabled(self, value): self._enabled = value
    def enabled(self): return self._enabled
    def set_initialized(self, value): self._initialized = value
    def initialized(self): return self._initialized
    def structured_output(self): return self._stuctured_output
    def linear_format(self): return self._linear_format
    def write_write_sync(self): return self._write_sync
    def source_mode(self): return self._source_mode
    def single_frame(self): return self._single_frame

    def path(self):
        if self._filename is not None:
            return self._filename.path().abs()
        return None

    def frames(self):
        # TODO: this could be optimized by a cache
        frames = []
        for scene in self.data:
            for frame in scene:
                frames.append(frame)
        return frames

    def fill_from_sources(self):
        source = None
        max_source_len = 0
        for cell in self.grid:
            if cell.source_seq() is not None:
                if cell.source_seq().data.total_length() > max_source_len:
                    max_source_len = cell.source_seq().data.total_length()
                    source = cell.source_seq()

        if source is None:
            return

        log.debug(f"Found source of length {max_source_len}")

        for scene in source.data:
            scene = self.data.scene(scene.name())
            for frame in scene:
                # This will automatically fill cells that have sources
                sample = scene.sample(frame.name())

        return self

    def read(self, filename=None):
        if filename is None:
            filename = self._filename
        if filename is None:
            raise Exception("Sequence.read() requires a filename")
        file = File(filename)
        self._filename = file

        log.debug(f"Reading sequence from '{file}'")
        if file.extension() == "json":
            read_json(self, file)
        elif file.extension() == "gridseq":
            read_gridseq(self, file)
        else:
            raise Exception(f"Don't know how to read file of type {file.extension()}")

        return self

    def write(self, filename=None, abs_path=False):
        if not self._enabled:
            return

        if filename is None:
            filename = self._filename
        if filename is None:
            raise Exception("Sequence.write() requires a filename")
        file = File(filename)
        self._filename = file

        log.debug(f"Writing sequence to '{file}'")
        if file.extension() == "json":
            write_json(self, file, abs_path)
        elif file.extension() == "gridseq":
            write_gridseq(self, file, abs_path)
        else:
            raise Exception(f"Don't know how to write file of type {file.extension()}")

        return self


