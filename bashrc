#!/bin/bash 

if [ -n "$ZSH_VERSION" ]; then
    export ITYPES_PATH="$( cd "$( dirname "${(%):-%N}" )" && pwd )"
else
    export ITYPES_PATH="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
fi

export PYTHONPATH="$ITYPES_PATH/python:$PYTHONPATH"
export PATH="$ITYPES_PATH/bin:$PATH"
