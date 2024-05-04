#!/bin/bash
#
# Read the parsed Sea-Bird Electronics Deep SeapHOx V2 data files from the CGSN
# Coastal Surface Moorings and create processed datasets available in NetCDF
# formatted files for further processing and review.
#
# C. Wingard 2024-02-20

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the pH"
    echo " directory name, the deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00018 44.63929 -124.30404 nsif/phtest 7 true 20161012.phtest.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
PH=${5,,}
DEPTH=$6
SWITCH=$7
FILE=$(basename $8)

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$PH/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$PH/${FILE%.json}.nc"
if [ ! -d $(dirname $OUT) ]; then
    mkdir -p $(dirname $OUT)
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_cphox -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -s $SWITCH -i $IN -o $OUT || echo "Processing failed for $IN"
fi
