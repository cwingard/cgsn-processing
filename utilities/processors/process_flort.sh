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
LAT=$3; LNG=$4
FLORT=${5,,}
CTD=${6,,}
DEPTH=$7
SERIAL=${8^^}
FILE=`/bin/basename $9`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python3"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$FLORT/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$FLORT/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$FLORT/flort_factory_calibration.coeffs"

# Process the file (if it hasn't already been done)
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_flort -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -dp $DEPTH \
        -i $IN -o $OUT -cf $COEFF -sn $SERIAL -df $CTD
fi
