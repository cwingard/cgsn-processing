#!/bin/bash
#
# Read the parsed SWND data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the SWND"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00018 44.63929 -124.30404 buoy/metwnd 20161012.metwnd.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
SWND=${5,,}
FILE=`basename $6`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$SWND/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$SWND/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_mopak -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp 4 \
      -i $IN -o $OUT || echo "Processing failed for $IN"
fi
