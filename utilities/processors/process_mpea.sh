#!/bin/bash
#
# Read the parsed MPEA data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the MPEA"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce07shsm D00007 46.98820 -124.56794 mfn/pwrsys 87 20161012.pwrsys.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
MPEA=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$MPEA/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$MPEA/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_mpea -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT
fi
