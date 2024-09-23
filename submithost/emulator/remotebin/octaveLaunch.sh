#!/bin/bash

# Executable launch script for the Pegasus workflow.
# Called with arguments: "$@"
echo "octaveLaunch.sh $@"

# "$@": ./filename1  arg1 ... argn,
# where filename1 is an octave script.

/usr/bin/octave --no-window-system --no-gui --no-history "$@"

:
