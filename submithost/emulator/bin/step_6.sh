#!/bin/bash

# Args:
# $1 - bin directory
# $2 - data directory
# $3 - sample number

#echo "step_6.sh "$1" "$2" "$3

bindir=$1
datadir=$2
samplenumber=$3

#echo $srcdir
#echo $datadir
#echo $numSamples

octave --no-window-system --no-gui --no-history --silent --eval \
   "cd $bindir; \
   extract_mini_emulator_build_meta_data('$datadir',$samplenumber);"
