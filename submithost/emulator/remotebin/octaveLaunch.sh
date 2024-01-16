#!/bin/bash

# Executable launch script for the Pegasus workflow.
# Called with argument: "$@"
echo "$@"

# "$@": ./filename1  arg1 ... argn,
# where filename1 is an octave script.

/usr/local/OCTAVE/4.0.0/bin/octave --no-window-system --no-gui --no-history "$@"

exitStatus=$?
exit ${exitStatus}

