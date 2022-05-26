#!/usr/bin/env python3

from itypes import Grid2D

g = Grid2D(none_in_range=True, none_outside_range=True)

g[1, 2] = "x"

print(f'min_col={g.min_col()} max_col={g.max_col()} num_cols={g.num_cols()} '
      f'min_row={g.min_row()} max_row={g.max_row()} num_rows={g.num_rows()}')

print(f'g[0, 0] = {g[0,0]}')
print(f'g[1, 2] = {g[1,2]}')
print(f'g[2, 2] = {g[2,2]}')

g[2, 2] = "y"

print(f'min_col={g.min_col()} max_col={g.max_col()} num_cols={g.num_cols()} '
      f'min_row={g.min_row()} max_row={g.max_row()} num_rows={g.num_rows()}')

print(f'g[0, 0] = {g[0,0]}')
print(f'g[1, 2] = {g[1,1]}')
print(f'g[2, 2] = {g[2,2]}')

del g[2, 2]

print(f'min_col={g.min_col()} max_col={g.max_col()} num_cols={g.num_cols()} '
      f'min_row={g.min_row()} max_row={g.max_row()} num_rows={g.num_rows()}')

