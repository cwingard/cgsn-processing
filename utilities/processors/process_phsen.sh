#!/bin/bash
#
# Read the parsed PHSEN data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in JSON formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and"
    echo "longitude, the PHSEN directory name, the name of the co-located CTD, the"
    echo "deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/phsen ctdbp 7 20161012.phsen.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
PHSEN=${5,,}
CTD=${6,,}
DEPTH=$7
FILE=`basename $8`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$PHSEN/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$PHSEN/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_phsen -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -df $CTD -i $IN -o $OUT
fi
