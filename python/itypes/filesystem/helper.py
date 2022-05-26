#!/usr/bin/env python3

import os

def split_path(path):
    parts = path.split('/')
    if len(parts) > 0:
        if parts[-1] == '':
            parts.pop(-1)
    return parts

def mkdirs(*parts):
    path = os.path.join(*parts)
    from .io import mkdirs
    mkdirs(path)
    return path
