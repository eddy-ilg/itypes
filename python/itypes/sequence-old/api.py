
seq = Sequence(file="..",
    folder="..", # checks default filenames
    cache_enabled=False,
    cache_size=X,
    cache_type="Proximity",
)

with seq.new_row() as row:
    row.add_cell()
    row.skip_cell()

with seq.new_col as col:
    ...

seq.add_cell(col, row, type, id, properties, source_seq, source_id,  title, source_method, cell)
seq.remove_cell(id, col, row, cell)

seq.ids()
seq.cell(id, row, col)
cell.id()
cell.type()
cell.row()
cell.col()
cell.properties()
cell.title()
cell.source_seq()
cell.source_id()
cell.source_method()

seq.add_cells(seq, source_method, placement="left")

with seq.new_group() as g:
    with seq.new_entry() as e:
        e.set_data(
            tensor | string | dataitem
        )
        e.set_reference(
            dataitem
        )

for entry in seq:
    ...

item = seq[idx, id]
item = seq[group, entry, id]

seq.group(name)

for group in seq.groups():
    for entry in group:
        ...

item.data()
item.properties()
item.files()




groups = seq.groups()
frames = group[x].frames()

from group in frame.groups():
    for frame in group:
        print(frame)

for frame in seq:
    print(frame)

len()

seq[idx]
seq[group_name, frame_name]

grid = seq.grid()

seq = grid.create_sequence()

seq = SequenceWriter(
    file="..",
    folder="..",
    grid,
    linear_format="",
    structured_output=False,


filename = None,
folder = None,
structured_output = True,
linear_format = "%08d-{id}",
write_sync = None,
source_mode = "copy", single_frame = False, enabled = True):


# Use cases:
# read seq and grid from file

# modify grid with sources
# create joined sequence
# write joined sequence
# read joined sequence without writing

# write seq fo file given grid and entries