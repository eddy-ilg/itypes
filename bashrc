#!/bin/bash 

ITYPES_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

export PYTHONPATH="$ITYPES_PATH/python:$PYTHONPATH"
export PATH="$ITYPES_PATH/bin:$PATH"
