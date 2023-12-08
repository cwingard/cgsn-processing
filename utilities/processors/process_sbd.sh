#!/bin/bash
#
# Read the parsed Iridium SBD messaging supervisor data files and
# create processed datasets available in NetCDF formatted files for
# further processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the"
    echo "latitude and longitude, the directory with the supervisor log, the"
    echo "deployment depth, a switch to indicate the type of supervisor"
    echo "(cpm or stc), and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00017 44.63929 -124.30404 buoy/sbd1 0 cpm 300234064920190.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
SBD=${5,,}
DEPTH=$6
SWITCH=${7,,}
FILE=`basename $8`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$SBD/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$SBD/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_sbd -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -s $SWITCH -i $IN -o $OUT
fi
