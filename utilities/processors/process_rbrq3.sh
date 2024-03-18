#!/bin/bash
#
# Read the parsed RBR/Q3 data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files.
#
# P. Whelan 2023-12-06

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the IFCB"
    echo "directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 cp10cnsm D0001 44.63929 -124.30404 nsif/rbrq3 7 1111 20231205.rbrq3.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
RBRQ3=${5,,}
DEPTH=$7
FILE=`basename $9`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$RBRQ3/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$RBRQ3/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file (if it hasn't already been done)
if [ -e $IN ]; then
    cd ../..
    {
        python -m cgsn_processing.process.proc_presf -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT -s rbrq3
    } || {
        echo "$IN failed to process"
    }
fi
