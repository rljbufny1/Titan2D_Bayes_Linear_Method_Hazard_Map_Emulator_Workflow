#!/bin/bash

# Bash script to update puffin.inp for each job.
# Adapted from dist-pcq.pl
# Called from Wrapper.py
# Needs executable bit set in svn:
# svn propset svn:executable on dist-pcq.sh

# Args:
# $1 - srcdir
# $2 - datadir
# $3 - workingdir
# $4 - PUFFINPUT_TEMPLATE
# $5 - PCQPOINTSFILE
# $6 - sampleno

#echo "dist-pcq.sh "$1" "$2" "$3" "$4" "$5" "$6

srcdir=$1
datadir=$2
workingdir=$3
PUFFINPUT_TEMPLATE=$4
PCQPOINTSFILE=$5
sampleno=$6

#echo $srcdir
#echo $datadir
#echo $workingdir
#echo $PUFFINPUT_TEMPLATE
#echo $PCQPOINTSFILE
#echo $sampleno

# .hysplitrc created by GUI so do not delete here
# hysplitargs created by GUI so do not delete here
# pcqsamplepoints created by GUI so do not delete here
# SondeFile.txt created by GUI so do not delete here

# Clean up submit generated files
if [[ $sampleno == 1 ]]; then
    rm -f driver*.xml
    rm -f run*.xml
    rm -f pegasus*
    rm -f *.stderr
    rm -f *.stdout
    rm -f results_*.mat
fi

jobdir=$(echo $(printf "$workingdir"))

# Create puffin.inp for this sample

# First line of sample data starts at line 1
lineno=$(( $sampleno ))
#echo $lineno

# Read and parse line of the PCQPOINTSFILE for this job

# sed expression -n $linenop will suppress default printing and just
# print line $lineno to the pattern buffer.  
# FYI, -n $p will just print the last line of the file
out=$(sed -n $lineno'p' < $PCQPOINTSFILE)
#echo $out

# format of PCQPOINTSFILE files:
# col1 = VENTRADIUS
# col2 = AXIALVELOCITY
# col3 = GRAINMEAN
# col4 = GRAINSDEV
# col5 = weights

# sed expression - 's/regexp/replacement/'
# \( - escaped left paren and \) - escaped right paren, remembers a pattern
# which can be recalled with \n where n is the number of the remembered pattern,
# up to 9 patterns can be remembered.
# next line is reading and storing the 1st number in a

VENTRADIUS=$(echo $out | sed 's/\(.*\) .* .* .* .*/\1/')
#echo $VENTRADIUS
AXIALVELOCITY=$(echo $out | sed 's/.* \(.*\) .* .* .*/\1/')
#echo $AXIALVELOCITY
GRAINMEAN=$(echo $out | sed 's/.* .* \(.*\) .* .*/\1/')
#echo $GRAINMEAN
GRAINSDEV=$(echo $out | sed 's/.* .* .* \(.*\) .*/\1/')
#echo $GRAINSDEV

puffin_inp=$(printf "$jobdir/puffin_sample_%03d.inp" $sampleno)
cp ${PUFFINPUT_TEMPLATE} $puffin_inp

#echostr=$(printf "Creating %s..." $puffin_inp)
#echo $echostr

#
# Use perl one-liners to adjust input parameters
#

perl -pi -e "s/VENTRADIUS\s*/VENTRADIUS ${VENTRADIUS}\n/" $puffin_inp
perl -pi -e "s/AXIALVELOCITY\s*/AXIALVELOCITY ${AXIALVELOCITY}\n/" $puffin_inp
perl -pi -e "s/GRAINMEAN\s*/GRAINMEAN ${GRAINMEAN}\n/" $puffin_inp
perl -pi -e "s/GRAINSDEV\s*/GRAINSDEV ${GRAINSDEV}\n/" $puffin_inp
