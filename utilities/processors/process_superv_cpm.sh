#!/bin/bash
#
# Read the parsed CPM SUPERV data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the CPM SUPERV"
    echo "directory name, the deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 buoy/superv/cpm1 0 20161012.superv.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
DEPTH=$5
SUPERV=${6,,}
FILE=`/bin/basename $7`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python3"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$SUPERV/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$SUPERV/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_superv_cpm -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -dp $DEPTH -i $IN -o $OUT
fi
