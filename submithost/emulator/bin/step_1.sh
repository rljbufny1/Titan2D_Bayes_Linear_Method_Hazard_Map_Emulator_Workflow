#!/bin/bash

# rlj - bash script to generate data for each sample

# Args:
# $1 - bin directory
# $2 - data directory
# $3 - number of samples

echo "step_1.sh "$1" "$2" "$3

bindir=$1
datadir=$2
numSamples=$3

#echo "bindir: "$bindir
#echo "datadir: "$datadir
#echo "numSamples: "$numSamples

octave=$(which octave)
echo "which octave: "${octave}

octave --no-window-system --no-gui --no-history --silent --eval \
   "cd $bindir; \
   Gen_Titan_Input_Samples('$datadir',$numSamples);"
