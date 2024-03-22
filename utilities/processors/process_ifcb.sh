#!/bin/bash
#
# Read the parsed IFCB data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files.
#
# P. Whelan 2023-12-06

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the IFCB"
    echo "directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 cp10cnsm D0001 44.63929 -124.30404 nsif/plims 7 20231205.ifcb.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
IFCB=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$IFCB/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$IFCB/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file (if it hasn't already been done)
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    {
        python -m cgsn_processing.process.proc_ifcb_hdr -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT
    } || {
        echo "$IN failed to process"
    }
fi
