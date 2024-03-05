#!/bin/bash
#
# Read the parsed ADCP data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the ADCP"
    echo " directory name, the name of the co-located CTD, the deployment depth and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/adcp ctdbp 7 20161012.adcpt.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
ADCP=${5,,}
CTD=${6,,}
DEPTH=$7
FILE=`basename $8`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$ADCP/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$ADCP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_adcp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON \
        -dp $DEPTH -i $IN -o $OUT -s pd0 -df $CTD || echo "Processing failed for $IN"
fi
