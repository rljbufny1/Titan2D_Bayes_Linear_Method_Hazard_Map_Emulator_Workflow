#!/bin/bash

# Args:
# $1 - matlab source directory
# $2 - data directory

#echo "step_5_8_9_10.sh: $@"

bindir=$1
datadir=$2

#echo $bindir
#echo $datadir

octave --no-window-system --no-gui --no-history --silent --eval \
    "cd $bindir; \
    script5_8_9_10('$datadir');"
