#!/bin/bash
#
# Read the parsed Iridium SBD messaging Xeos beacon data files and
# create processed datasets available in NetCDF formatted files for
# further processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the"
    echo "latitude and longitude, the directory with the Xeos beacon log, the"
    echo "deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00017 44.63929 -124.30404 buoy/xeos1 0 300434062471920.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
XEOS=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$XEOS/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$XEOS/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_xeos -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT
fi
