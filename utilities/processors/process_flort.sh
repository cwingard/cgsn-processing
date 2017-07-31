#!/bin/bash
#
# Read the parsed FLORT data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied, rough temperature and salinity 
# corrections (for now) and an initial scatter correction for further 
# processing and review.
#
# C. Wingard 2017-01-23

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the FLORT"
    echo "directory name, the serial number of the unit, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/flort 1153 20161012.flort.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
FLORT=${5,,}
SERIAL=${6^^}
CFILE="${PLATFORM^^}_$DEPLOY_FLORT_$SERIAL.coeff"
FILE=`/bin/basename $7`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python3"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$FLORT/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$FLORT/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$FLORT/$CFILE"

# Process the file (if it hasn't already been done)
if [ -e $IN ] && [ ! -e $OUT ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_flort -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT -cf $COEFF -sn $SERIAL
fi
