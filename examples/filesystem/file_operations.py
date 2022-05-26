#!/usr/bin/env python3

from itypes import Path, File

file = Path('data').file('text.txt')
print()

# Creating <File> objects
print(f"Path('data').file('text.txt'):       {Path('data').file('text.txt')}")
print(f"Path('data').file('text.txt').abs(): {Path('data').file('text.txt').abs()}")
print(f"File('data/text.txt'):               {File('data/text.txt')}")
print(f"File('data/text.txt').abs():         {File('data/text.txt').abs()}")
print()

# Lots of operations
print(f"file:                                           {file}")
print(f"file.extension():                               {file.extension()}")
print(f"file.name():                                    {file.name()}")
print(f"file.basename():                                {file.basename()}")
print(f"file.exists():                                  {file.exists()}")
print(f"file.path():                                    {file.path()}")
print(f"file.path().abs():                              {file.path().abs()}")
print(f"file.rel_to('subdir/x'):                        {file.rel_to('subdir/x')}")
print(f"file.replace_extension():                       {file.replace_extension('textfile')}")
print(f"file.add_suffix('0000'):                        {file.add_suffix('0000')}")
print(f"file.add_suffix('0000', sep='-'):               {file.add_suffix('0000', sep='-')}")
print(f"file.add_suffix('0000', sep='.'):               {file.add_suffix('0000', sep='.')}")
print(f"Path('data').file('text.0000.txt').extension(): {file.add_suffix('0000', sep='.').extension()}")
print()

# write, remove
file = Path('out_file_operations').file('test.txt')
file.write('Test Content')
print(f"Path('out_file_operations').file('test').exists() after write: {Path('out_file_operations').file('test.txt').exists()}")
print("Note that the write triggered making the parent directories.")
file.remove()
print(f"Path('out_file_operations').file('test').exists() after remove: {Path('out_file_operations').file('test.txt').exists()}")
Path('out_file_operations').remove()
print()

# index(), str_index()
file = Path('out_file_operations_00005').file('test-0003.txt')
print(f"Path('out_file_operations_00005').file('test-0003.txt').index():     {file.index()}")
print(f"Path('out_file_operations_00005').file('test-0003.txt').str_index(): {file.str_index()}")
print()

# copy_to()
file = File('out_file_operations/test1.txt')
file.write("Test Content")
file.copy_to(File('out_file_operations/test2.txt'))
file.copy_to('out_file_operations/test3.txt')
print('out_file_operations contents after copying:')
for file in Path("out_file_operations").list_files():
    print(file)
Path('out_file_operations').remove()
print()

# Todo open
# Todo equal
# Todo add move
