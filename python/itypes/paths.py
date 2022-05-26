#!/usr/bin/env python3

from .filesystem import File


itypes_root = File(__file__).path().cd('..').cd('..').abs()
exapmles_root = itypes_root.cd('examples').abs()
data_root = exapmles_root.cd('data').abs()