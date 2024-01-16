#!/bin/bash

# Args:
# $1 - matlab source directory, <tool>/bin
# $2 - data directory

echo "step_15.sh "$1" "$2" "$3

bindir=$1
datadir=$2
workingdir=$3

#echo $bindir
#echo $datadir
#echo $workingdir

# With --no-window-system, default and only available graphics_toolkit is gnuplot, need qt
octave --no-window-system --no-history --silent --eval \
    "cd $bindir; \
    view_phm('$datadir','$workingdir');"
