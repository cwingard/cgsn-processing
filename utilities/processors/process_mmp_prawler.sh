#!/bin/bash
#
# Read the parsed Prawler MMP data files from the CGSN Shallow Water Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# P. Whelan   2024-05-08

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the prawler"
    echo " directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 cp12wesw D0001 35.94979 -75.12554 imm/prkt 30 prkt_202540502_130021.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3;
LON=$4
PRAWLER=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$PRAWLER/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$PRAWLER/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_mmp_prawler -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT
fi
