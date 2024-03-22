#!/bin/bash
#
# Read the parsed PRTSZ data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# S. Dahlberg 2024-02-01

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the PRTSZ"
    echo " directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 cp11sosm D00001 44.63929 -124.30404 dcl/prtsz 82 20240201.prtsz.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
PRTSZ=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$PRTSZ/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$PRTSZ/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_prtsz -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT
fi
