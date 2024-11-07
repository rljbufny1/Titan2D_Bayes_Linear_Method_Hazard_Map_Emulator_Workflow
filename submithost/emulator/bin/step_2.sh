#!/bin/bash

# rlj - bash script to update the Titan2D input file for each sample

# Args:
# $1 - workingdir
# $2 - titan2dInputFile
# $3 - samplenumber

#echo "step_2.sh: $@"

workingdir=$1
titan2dInputFile=$2
samplenumber=$3

#echo "working_dir: "$workingdir
#echo "titan2dInputFile: "$titan2dInputFile
#echo "samplenumber: "$samplenumber

# Modify simulation.py for this sample

# uncertain_input_list_h.txt data line number for this sample.
# First line of sample data starts at line 7
lineno=$(( $samplenumber + 6 ))
#echo $lineno

# Read and parse line of uncertain_input_list_h.txt for this sample

# sed expression -n $linenop will suppress default printing and just
# print line $lineno to the pattern buffer.  
# FYI, -n $p will just print the last line of the file
out=$(sed -n $lineno'p' < $workingdir/uncertain_input_list_h.txt)
#echo $out

# sed expression - 's/regexp/replacement/'
# \( - escaped left paren and \) - escaped right paren, remembers a pattern
# which can be recalled with \n where n is the number of the remembered pattern,
# up to 9 patterns can be remembered.
# next line is reading and storing the 1st number in a
# a: h [m]
a=$(echo $out | sed 's/\(.*\) .* .* .* .*/\1/')
#echo $a
# next line is reading and storing the 2nd number in b ...
# b: radius [m]
b=$(echo $out | sed 's/.* \(.*\) .* .* .*/\1/')
#echo $b
# c: UTME
c=$(echo $out | sed 's/.* .* \(.*\) .* .*/\1/')
#echo $c
# d: UTMN
d=$(echo $out | sed 's/.* .* .* \(.*\) .*/\1/')
#echo $d
# e: BedFrictAng [deg]
e=$(echo $out | sed 's/.* .* .* .* \(.*\)/\1/')
#echo $e

# Create simulation.py for this sample

simulation_filename=$(printf "simulation_%06d.py" $samplenumber)

#echostr=$(printf "Creating %s..." $simulation_filename)
#echo $echostr

if [ -f  $workingdir/temp.py ]; then
   #echo "Removing temp.py"
   rm $workingdir/temp.py
fi

filename=$workingdir/temp.py
#echo $filename

# Update simulation.py for this sample

# Keep leading white space for file output.
# Set the internal field separator
IFS=''

firstmatmodelbedfrict=0
firststatpropsrunid=0
firstpileheight=0
firstpilecenter=0
firstpileradii=0
oscommandfound=0

while read data; do

   nextline=$data
   #echo $nextline

   # Trim leading white space for check.
   # ^[ \t]* : search pattern ( ^ - start of the line; 
   # [ \t]* match one or more blank spaces including tab
   trimmed=$(echo $nextline | sed -e "s/^[ \t]*//")
   #echo $trimmed

   # sim.setGIS

   if [[ $trimmed == "os"* ]]
   then

      oscommandfound=1
      break
   
   elif [[ $trimmed == "gis_main"* ]]
   then

      gis_main=$nextline
      # Get the sting between the quotes:
      # http://www.unix.com/shell-programming-and-scripting/127672-extracting-text-between-quotes.html
      gis_main=$(echo $gis_main | sed "s/.*'\(.*\)'[^']*$/\1/")
      #echo $gis_main

      # Extract the last subdirectory name from the full path name
      gis_main=$(basename $gis_main)
      #echo $gis_main

      # Make the grass directory names consistent.
      # Also see setup.sh
      newline=$"   gis_main='"./grassdata"',"
      #echo $newline
      echo $newline >> $filename

   # sim.setMatModel:

   elif [[ $trimmed == "bed_frict="* ]]
   then

      if [[ $firstmatmodelbedfrict == 0 ]]
      then
         firstmatmodelbedfrict=1
         newline=$(echo $nextline | sed "s/bed_frict=.*/bed_frict=$e/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   # sim.setStatProps:

   elif [[ $trimmed == "runid="* ]]
   then

      if [[ $firststatpropsrunid == 0 ]]
      then
         firststatpropsrunid=1
         samplenumberstr=$(printf "%d" $samplenumber)
         newline=$(echo $nextline | sed "s/runid=-1/runid=$samplenumberstr/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   # sim.addPile:

   elif [[ $trimmed == "height="* ]]
   then

      if [[ $firstpileheight == 0 ]]
      then
         firstpileheight=1
         newline=$(echo $nextline | sed "s/height=.*,/height=$a,/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   elif [[ $trimmed == "center="* ]]
   then

      if [[ $firstpilecenter == 0 ]]
      then
         firstpilecenter=1
         newline=$(echo $nextline | sed "s/center=\[.*, .*\],/center=\[$c, $d\],/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   elif [[ $trimmed == "radii="* ]]
   then

      if [[ $firstpileradii == 0 ]]
      then
         firstpileradii=1
         newline=$(echo $nextline | sed "s/radii=\[.*, .*\],/radii=\[$b, $b\],/")
         #echo $newline
         echo $newline >> $filename
      else
         echo $nextline >> $filename
      fi

   else
      echo $nextline >> $filename
   fi

done < $titan2dInputFile

if [[ $oscommandfound == 0 ]] 
then
   mv $filename $workingdir/$simulation_filename
   chmod 664 $workingdir/$simulation_filename
else
   echo "Python commands beginning with os are not allowed in simulation.py"
fi   
