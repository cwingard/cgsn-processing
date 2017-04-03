#!/bin/bash
#
# Read the parsed CPM SUPERV data files from the Endurance Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the CPM SUPERV"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 buoy/superv/cpm1 20161012.superv.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
SUPERV=${5,,}
FILE=`/bin/basename $6`

# Set the default directory paths and input/output sources
PYTHON="/home/cgsnmo/anaconda3/envs/ooi/bin/python"

DATA="/webdata/cgsn/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$SUPERV/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$SUPERV/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/cgsnmo/dev/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_superv_cpm -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT
fi
