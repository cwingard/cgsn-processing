#!/bin/bash
#
# Read the parsed NUTNR data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-10-30

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the NUTNR"
    echo "directory name, the name of the co-located CTD, the deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 ce01issm D00008 44.63929 -124.30404 nsif/nutnr ctdbp1 7 20161012.nutnr.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
NUTNR=${5,,}
CTD=${6,,}
DEPTH=$7
FILE=`basename $8`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$NUTNR/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$NUTNR/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$NUTNR/nutnr_inhouse_calibration.coeffs"

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_suna -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT \
        -cf $COEFF -df $CTD
fi
