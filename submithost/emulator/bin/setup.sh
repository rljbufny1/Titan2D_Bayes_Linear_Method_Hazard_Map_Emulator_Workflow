#!/bin/bash

# Args:
# $1 - working directory
# $2 - matlab source directory, <tool>/bin
# $3 - data directory <tool>/data
# $4 - titan2dInputFile
# $5 - titan2dInputFiled
# $6 - titan2dInputFiledd
# $7 - user minvol value
# $8 - user maxvol value
# $9 - user BEDMIN value
# $10 - user BEDMAX value
# $11 - user STARTUTMECEN value
# $12 - user STARTUTMNCEN value
# $13 - user STARTRADIUSMAX value
# $14 - user ResamplePoints value
# $15 - numSamples

# double digits need {}
echo "setup.sh "${1}" "${2}" "${3}" "${4}" "${5}" "${6}" "${7}" "${8}" "${9}" "${10}" "${11}" "${12}" "${13}" "${14}" "${15}

workingdir=${1}
bindir=${2}
datadir=${3}
titan2dInputFile=${4}
titan2dInputFiled=${5}
titan2dInputFiledd=${6}
minvol=${7}
maxvol=${8}
BEDMIN=${9}
BEDMAX=${10}
STARTUTMECEN=${11}
STARTUTMNCEN=${12}
STARTRADIUSMAX=${13}
ResamplePoints=${14}
numSamples=${15}

#echo "workingdir: "$workingdir
#echo "bindir: "$bindir
#echo "datadir: "$datadir
#echo $titan2dInputFile
#echo $titan2dInputFiled
#echo $titan2dInputFiledd
#echo "minvol: "$minvol
#echo "maxvol: "$maxvol
#echo "BEDMIN: "$BEDMIN
#echo "BEDMAX: "$BEDMAX
#echo "STARTUTMECEN: "$STARTUTMECEN
#echo "STARTUTMNCEN: "$STARTUTMNCEN
#echo "STARTRADIUSMAX: "$STARTRADIUSMAX
#echo "ResamplePoints: "$ResamplePoints
#echo "numSamples: "$numSamples

# Clean up submit generated files
rm -rf grassdir*
rm -f .__time_results.*
rm -f driver*.xml
rm -f run*.xml
rm -f octave_ID*.stdout
rm -f octave_ID*.stderr
rm -f titan_ID*.stdout
rm -f titan_ID*.stderr
rm -f runParams*.mat
rm -f uncertain*.txt
rm -f simulation*.py
rm -f macro_emulator.pwem
rm -f macro_resmaples.tmp
rm -f macro_resample_assemble.inputs
rm -f AZ_vol_dir_bed_int.phm
rm -f step11_12_13_staged_input.txt
rm -f workflow.yml
#rm -f pegasus*
#rm -f P.png
rm -f P.txt
#rm -f SDP.png
rm -f SDP.txt

echo $(printf "Processing Titan2D input file: %s" $titan2dInputFile)

# Keep leading white space for file output.
# Set the internal field separator
IFS=''

# Verify file format

simBeginFound=-1
simEndFound=-1

while read data; do

   nextline=$data
   #echo $nextline

   # Trim leading white space for check.
   # ^[ \t]* : search pattern ( ^ - start of the line; 
   # [ \t]* match one or more blank spaces including tab
   trimmed=$(echo $nextline | sed -e "s/^[ \t]*//")
   #echo $trimmed

   # Verify Titan2d input file format
   
   # sim=TitanSimulation()
   if [[ $trimmed == "sim=TitanSimulation"* ]]
   then
      simBeginFound=1

   # sim=sim.run()
   elif [[ $trimmed == "sim=sim.run"* ]]
   then
      simEndFound=1

   fi

done < $titan2dInputFile

if [[ $simBeginFound != 1 ]] 
then
   echo $(printf "Titan2D input file: %s parsing error: sim=TitanSimulation() not found" \
      $titan2dInputFile)
   exit 1
fi

if [[ $simEndFound != 1 ]]
then
   echo $(printf "Titan2D input file %s parsing error: sim=sim.run() not found" \
      $titan2dInputFile)
   exit 1
fi   

# Verify GRASS input directories.
# Make GRASS directories and copy required files to them.
# Note this is for GRASS GIS simulation.py files, GRASS GDAL simulation.py files are different

west=-1
east=-1
south=-1
north=-1
ewresol=-1
nsresol=-1

# Comprise grass subdirectories specified in the Titan2D Iinput file

mapsetdir=""

# Comprise required compute node subdirectories

cpumapsetdir=$workingdir
#echo $cpumapsetdir

# Parse simulation.py.
# Modify simulation.py for a 10 step run to
# create a pileheightrecord for retrieving the grid dimensions

if [ -f  $workingdir/temp.py ]; then
   #echo "Removing temp.py"
   rm $workingdir/temp.py
fi

filename=$workingdir/temp.py
#echo $filename

firstmaxiter=0

while read data; do

   nextline=$data
   echo $nextline

   # Trim leading white space for check.
   # ^[ \t]* : search pattern ( ^ - start of the line; 
   # [ \t]* match one or more blank spaces including tab
   trimmed=$(echo $nextline | sed -e "s/^[ \t]*//")
   #echo $trimmed

   # sim.setGIS

   if [[ $trimmed == "gis_main"* ]]
   then

      # Make the required grass directories and copy required files to them
      gis_main=$nextline
      # Reference:
      # Get the string between the quotes:
      # http://www.unix.com/shell-programming-and-scripting/127672-extracting-text-between-quotes.html
      gis_main=$(echo $gis_main | sed "s/.*'\(.*\)'[^']*$/\1/")
      #echo $gis_main

      # Check for relative paths
      # References:
      # http://tldp.org/LDP/abs/html/textproc.html
      # http://www.computerhope.com/unix/ucut.htm
      # http://www.thegeekstuff.com/2010/07/bash-string-manipulation/

      gis_main_len=$(echo ${#gis_main})
      #echo $gis_main_len

      BASE_DIRECTORY=$(echo "$gis_main" | cut -d "/" -f1)
      #echo $BASE_DIRECTORY

      # Compare to the last subdirectory name from the full path name
      if [[ $BASE_DIRECTORY == $(basename $gis_main) ]]
      then
         echo "gis_main offset from <Titan2D input file> resolved"
         gis_main=$titan2dInputFiled/$(echo ${gis_main:0:$gis_main_len})
         echo $gis_main
  
      elif [[ $BASE_DIRECTORY == "." ]]
      then

         echo "gis_main offset from ./<Titan2D input file> resolved"
         gis_main=$titan2dInputFiled/$(echo ${gis_main:2:$gis_main_len})
         echo $gis_main

      elif [[ $BASE_DIRECTORY == ".." ]]
      then

         echo "gis_main offset from ../<Titan2D input file> resolved"
         gis_main=$titan2dInputFiledd/$(echo ${gis_main:3:$gis_main_len})
         echo $gis_main

      fi
      
      # mapsetdir is the copy from directory
      mapsetdir=$gis_main

      #echo $gis_main
      #echo $mapsetdir
 
      # Extract the last subdirectory name from the full path name
      gis_main=$(basename $gis_main)
 
      # Make the grass directory names consistent.
      # cpumapsetdir is the copy to directory
      #cpumapsetdir=$cpumapsetdir/$gis_main
      cpumapsetdir=$cpumapsetdir/"grassdir"
      #echo $cpumapsetdir
      echostr=$(printf "renaming gis_main GRASS directory from %s to grassdir" $gis_main)
      #echo $echostr
 
      # Make required grass subdirectory

      mkdir -p $cpumapsetdir
      # Hard set.
      # Will change when code to download and create the grass directory is done
      thisline="   gis_main='./grassdata',"
echo $thisline >> $filename
  
   elif [[ $trimmed == "gis_sub"* ]]
   then

      gis_sub=$nextline
      gis_sub=$(echo $gis_sub | sed "s/.*'\(.*\)'[^']*$/\1/")
      #echo $gis_sub

      mapsetdir=$mapsetdir/$gis_sub
 
      #echo $mapsetdir

      cpumapsetdir=$cpumapsetdir/$gis_sub
 
      #echo $cpumapsetdir
 
      # Make required grass subdirectory

      mkdir -p $cpumapsetdir
      echo $nextline >> $filename

   elif [[ $trimmed == "gis_mapset"* ]]
   then

      gis_mapset=$nextline
      gis_mapset=$(echo $gis_mapset | sed "s/.*'\(.*\)'[^']*$/\1/")
      #echo $gis_mapset

      cellhddir="$mapsetdir/$gis_mapset/cellhd"
      fcelldir="$mapsetdir/$gis_mapset/fcell"
      vectordir="$mapsetdir/$gis_mapset/vector"

      #echo $cellhddir
      #echo $celldir
      #echo $vectordir

      # Make the required grass subdirectories

      cpumapdir=$cpumapsetdir/$gis_mapset

      #echo $cpumapdir

      mkdir -p $cpumapdir

      cpucellhddir="$cpumapdir/cellhd"
      cpufcelldir="$cpumapdir/fcell"
      cpuvectordir="$cpumapdir/vector"

      #echo $cpucellhddir
      #echo $cpufcelldir
      #echo $cpuvectordir

      mkdir -p $cpucellhddir
      mkdir -p $cpufcelldir
      mkdir -p $cpuvectordir
      echo $nextline >> $filename

   elif [[ $trimmed == "gis_map"* ]]
   then

      gis_map=$nextline
      gis_map=$(echo $gis_map | sed "s/.*'\(.*\)'[^']*$/\1/")
      #echo $gis_map

      # Copy the cellhd and fcell files to the grass directories

      cellhdfile=$cellhddir/$gis_map
      fcellfile=$fcelldir/$gis_map

      #echo $cellhdfile
      #echo $fcellfile

      cpucellhdfile=$cpucellhddir/$gis_map
      cpufcellfile=$cpufcelldir/$gis_map

      #echo $cpucellhdfile
      #echo $cpufcellfile

      # Verify access to the cellhd and fcell directories
      cp -f $cellhdfile $cpucellhdfile
      if [ $? -ne 0 ]
      then
         echo "The GRASS cellhd directory not found"
         exit 1
      fi 

      cp -f $fcellfile $cpufcellfile
      if [ $? -ne 0 ]
      then
         echo "The GRASS fcell directory not found"
         exit 1
      fi 

      # Read cellhdfile and get north,south,east,west

      while read cdata; do

          cnextline=$cdata
          #echo $cnextline

          # Trim leading white space for check.
          # ^[ \t]* : search pattern ( ^ - start of the line; 
          # [ \t]* match one or more blank spaces including tab
          ctrimmed=$(echo $cnextline | sed -e "s/^[ \t]*//")
          #echo $ctrimmed

          if [[ $ctrimmed == "north:"* ]]
          then
             val=$(echo $cnextline | sed 's/north:\(.*\)/\1/')
             # trim leading white space
             north=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "north: "$north
          elif [[ $ctrimmed == "south:"* ]]
          then
             val=$(echo $cnextline | sed 's/south:\(.*\)/\1/')
             # trim leading white space
             south=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "south: "$south
          elif [[ $ctrimmed == "east:"* ]]
          then
             val=$(echo $cnextline | sed 's/east:\(.*\)/\1/')
             # trim leading white space
             east=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "east: "$east
          elif [[ $ctrimmed == "west:"* ]]
          then
             val=$(echo $cnextline | sed 's/west:\(.*\)/\1/')
             # trim leading white space
             west=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "west: "$west
          elif [[ $ctrimmed == "e-w resol:"* ]]
          then
             val=$(echo $cnextline | sed 's/e-w resol:\(.*\)/\1/')
             # trim leading white space
             ewresol=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "ewresol: "$ewresol
          elif [[ $ctrimmed == "n-s resol:"* ]]
          then
             val=$(echo $cnextline | sed 's/n-s resol:\(.*\)/\1/')
             # trim leading white space
             nsresol=$(echo $val | sed -e "s/^[ \t]*//")
             #echo "nsresol: "$nsresol
          fi
     done < $cpucellhdfile
     echo $nextline >> $filename

   elif [[ $trimmed == "gis_vector"* ]]
   then

      gis_vector=$nextline
      #echo $gis_vector

      # need quotes so not possible to check blank == "gis_vector=None,"
      if [[ "$gis_vector" != "    gis_vector=None," ]]; then

         gis_vector=$(echo $gis_vector | sed "s/.*'\(.*\)'[^']*$/\1/")
         #echo $gis_vector

         if [[ "$gis_vector" != "" ]]; then

            # Copy the vector file to the grass directory

            vectorfile=$vectordir/$gis_vector

            #echo $vectorfile

            cpuvectorfile=$cpuvectordir/$gis_vector

            echo $cpuvectorfile

            cp -f $vectorfile $cpuvectorfile
         fi
         echo $nextline >> $filename
      fi

   elif [[ $trimmed == "max_iter="* ]]
   then

      if [[ $firstmaxiter == 0 ]]
      then
         firstmaxiter=1
         newline=$(echo $nextline | sed "s/max_iter=.*,/max_iter=10,/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   else
      echo $nextline >> $filename
   fi

done < $titan2dInputFile

mv $filename $workingdir/simulation_init.py

echo "pwd: "$(pwd)

# Enable the use command
# . and source are the same
#. /etc/environ.sh

# Create runParams.mat
octave=$(which octave)
echo ${octave}

echo 'runParams...'
octave --no-window-system --no-gui --no-history --silent --eval \
    "cd $bindir; \
    runParams('$workingdir',$minvol,$maxvol,$BEDMIN,$BEDMAX,\
    $STARTUTMECEN, $STARTUTMNCEN, $STARTRADIUSMAX, $ResamplePoints,\
    $west, $east, $south, $north, $ewresol, $nsresol);"
echo 'Done'
