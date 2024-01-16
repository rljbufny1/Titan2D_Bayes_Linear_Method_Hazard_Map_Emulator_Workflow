#!/bin/bash

# Args:
# $1 - matlab source directory
# $2 - data directory

#echo "step_11_12_13_stage.sh "$1" "$2" "$3

srcdir=$1
datadir=$2

#echo $srcdir
#echo $datadir

octave --no-window-system --no-gui --no-history --silent --eval \
    "cd $srcdir; \
    script11_12_13_stage('$datadir');"
