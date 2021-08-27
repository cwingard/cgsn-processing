#!/bin/bash
#
# Read the parsed DOSTA data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the DOSTA"
    echo " directory name, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/dosta 7 20161012.dosta.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
DOSTA=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$DOSTA/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$DOSTA/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_dosta -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -ba -i $IN -o $OUT
fi
