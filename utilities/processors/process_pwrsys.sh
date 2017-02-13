#!/bin/bash
#
# Read the parsed buoy Power System Controller (PSC, or pwrsys) data files from
# the Endurance Surface Moorings and create processed datasets available in 
# NetCDF formatted files for further processing and review.
#
# C. Wingard 2017-02-11

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the"
    echo " PWRSYS directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 buoy/pwrsys 20161012.pwrsys.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
PWRSYS=${5,,}
FILE=`/bin/basename $6`

# Set the default directory paths and input/output sources
BIN="/home/cgsnmo/dev/cgsn-parsers/cgsn_parsers/process"
PYTHON="/home/cgsnmo/anaconda3/envs/py27/bin/python"

DATA="/webdata/cgsn/data/proc"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$PWRSYS/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$PWRSYS/${FILE%.json}.nc"

# Process the file
if [ -e $IN ]; then
    $PYTHON -m $BIN/proc_pwrsys --p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG i $IN -o $OUT
fi
