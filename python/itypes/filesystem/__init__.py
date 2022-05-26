#!/usr/bin/env python3

from .io import read
from .io import write
from .io import register_read_function
from .io import register_write_function
from .io import register_file_system
from .io import unregister_file_system

from .read_parallel import read_parallel

from .file import File

from .path import Path
from .path import home

from .memory import MemoryFileSystem