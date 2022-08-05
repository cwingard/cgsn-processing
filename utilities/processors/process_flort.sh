#!/bin/bash
#
# Read the parsed FLORT data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied, and the temperature and salinity
# corrected total optical backscatter calculated for further processing and review.
#
# C. Wingard 2017-01-23

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the FLORT"
    echo "directory name, the name of the co-located CTD, the deployment depth, the serial number of the unit,"
    echo "and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/flort ctdbp 7 1153 20161012.flort.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
FLORT=${5,,}
CTD=${6,,}
DEPTH=$7
SERIAL=${8^^}
FILE=`basename $9`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$FLORT/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$FLORT/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file (if it hasn't already been done)
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    {
        python -m cgsn_processing.process.proc_flort -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
            -i $IN -o $OUT -sn $SERIAL -df $CTD -ba
    } || {
        echo "$IN failed to process"
    }
fi
