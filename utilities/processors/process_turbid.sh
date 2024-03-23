#!/bin/bash
#
# Read the parsed TURBD data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2023-03-03

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the TURBD"
    echo " directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 as03cpsm D0001 35.94979 -75.12554 nsif/turbd 7 20230303.turbd.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
TURBD=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$TURBD/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$TURBD/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_turbd -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN_FILE -o $OUT_FILE
fi
