#!/usr/bin/env python3

from .io import read
from multiprocessing.dummy import Pool as ThreadPool

def read_parallel(urls, num_threads=64, **kwargs):
    def read_with_args(url):
        return read(url, **kwargs)

    pool = ThreadPool(num_threads)
    result = pool.map(read_with_args, urls)
    return result

