#!/bin/bash
#
# Read the parsed Coastal MMP data files from the Profiler Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the MMP"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce09ospm D00006 46.85165 -124.98229 imm/mmp P0000125.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
MMP=${5,,}
FILE=`basename $6`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$MMP/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$MMP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the profile dataset
if [ -e $IN ] && [ ! -e ${OUT%.nc}-edata.nc ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_mmp_coastal -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -i $IN -o $OUT
fi
