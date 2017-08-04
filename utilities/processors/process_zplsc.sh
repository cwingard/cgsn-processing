#!/bin/bash
#
# Read the parsed ZPLSC data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the ZPLSC directory"
    echo "name, the deployment depth, then bin size of the condensed bins and the name of the file to process."
    echo ""
    echo "     example: $0 ce07shsm D00004 46.986 124.566 mfn/zplsc 87 5.016 20161012.zplsc.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
ZPLSC=${5,,}
DEPTH=$6
BINSIZE=$7
FILE=`/bin/basename $8`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python3"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$ZPLSC/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$ZPLSC/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_zplsc -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -dp $DEPTH -bs $BINSIZE -i $IN -o $OUT
fi
