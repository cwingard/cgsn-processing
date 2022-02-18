#!/bin/bash
#
# Read the parsed CPM SUPERV data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the"
    echo "latitude and longitude, the supervisor log directory name, the"
    echo "deployment depth, a switch to indicate the type of supervisor log"
    echo "(cpm, dcl, or stc), and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 buoy/superv/cpm1 0 cpm 20161012.superv.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
SUPERV=${5,,}
DEPTH=$6
SWITCH=${7,,}
FILE=`basename $8`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$SUPERV/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$SUPERV/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_superv -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -s $SWITCH -i $IN -o $OUT
fi
