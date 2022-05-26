#!/usr/bin/env python3

import logging
from collections import OrderedDict
from ..filesystem import File

log = logging.getLogger('sequence_io')


def read_gridseq(seq, file):
    with file.open('r') as f:
        lines = f.read().split("\n")

        # Get grid definition
        for line in lines:
            if line.startswith("def"):
                parts = line.split(" ")
                col = int(parts[1])
                row = int(parts[2])
                id = parts[3].replace("<", "").replace(">", "")
                type = parts[4]
                title = None
                if len(parts)>5:
                    title = ' '.join(parts[5:])
                seq.grid[(col, row)] = seq.grid.Cell(seq.grid, type, id, title=title)

        # Get data definition
        scenes = OrderedDict()
        scene_counter = 0
        frame_counter = 0

        def add(scene_name, frame_name, fills):
            nonlocal scenes
            nonlocal scene_counter
            nonlocal frame_counter

            if scene_name is None:
                scene_name = "scene%d" % scene_counter
                scene_counter += 1

            if frame_name is None:
                frame_name = "frame%d" % frame_counter
                frame_counter += 1

            if scene_name not in scenes:
                scenes[scene_name] = OrderedDict()

            scenes[scene_name][frame_name] = fills

        current_entry_name = None
        current_set_name = None
        current_fills = OrderedDict()
        for line in lines:
            parts = line.split(" ")
            if line.startswith("fill"):
                id = parts[1].replace("<", "").replace(">", "")
                if parts[2] == 'None': data_file = None
                else: data_file = File(parts[2])
                current_fills[id] = data_file
            elif line.startswith("set_name"):
                current_set_name = parts[1]
            elif line.startswith("entry_name"):
                current_entry_name = parts[1]
            elif line.startswith("next"):
                add(current_set_name, current_entry_name, current_fills)
                current_fills = OrderedDict()
                current_entry_name = None
                current_set_name = None

        if len(current_fills):
            add(current_set_name, current_entry_name, current_fills)

        for scene_name, frames in scenes.items():
            scene = seq.data.scene(scene_name)
            for frame_name, ids in frames.items():
                frame = scene.sample(frame_name)
                for id, data_file in ids.items():
                    if data_file is None:
                        frame.set_data(id, None)
                    else:
                        frame.set_ext(id, file.path() + data_file, check_if_exists=False)


def read_json(seq, file):
    raise NotImplementedError

def write_gridseq(seq, file, abs_path=False):
    with file.open('w') as f:
        for pos, cell in seq.grid.items():
            f.write('def %d %d <%s> %s %s\n' % (pos[0], pos[1], cell.id(), cell.type(), '' if cell.title() is None else cell.title()))
        for scene_name, scene in seq.data.items():
            for frame_name, frame in scene.items():
                for id, data in frame.items():
                    data.set_base_path(file.path())
                    data.write_sync()
                    if data.file() is None:
                        f.write('fill <%s> %s\n' % (id, None))
                        continue
                    data_file = data.file() if abs_path else data.file().rel_to(file.path())
                    f.write('fill <%s> %s\n' % (id, data_file))
                f.write("set_name %s\n" % scene_name)
                f.write("entry_name %s\n" % frame_name)
                f.write("next\n")

def write_json(seq, file, abs_path=False):
    pass