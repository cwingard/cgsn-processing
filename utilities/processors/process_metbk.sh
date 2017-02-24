#!/bin/bash
#
# Read the parsed METBK data files from the Endurance Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the METBK"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 buoy/metbk 20161012.metbk.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
METBK=${5,,}
FILE=`/bin/basename $6`

# Set the default directory paths and input/output sources
BIN="/home/cgsnmo/dev/cgsn-processing/cgsn_processing/process"
PYTHON="/home/cgsnmo/anaconda3/envs/py27/bin/python"

DATA="/webdata/cgsn/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$METBK/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$METBK/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    $PYTHON -m $BIN/proc_metbk -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT
fi
