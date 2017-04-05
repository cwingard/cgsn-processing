#!/bin/bash
#
# Read the parsed SPKIR data files from the Endurance Surface Moorings and 
# create processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied, rough temperature and salinity 
# corrections (for now) and an initial scatter correction for further 
# processing and review.
#
# C. Wingard 2017-01-23

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the SPKIR"
    echo "directory name, the UID name of the stored factory calibration data, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/spkir SPKIRB/CGINS-SPKIRB-00242__20160926 20161012.spkir.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
SPKIR=${5,,}
UID=${6^^}
CFILE=`/bin/basename $UID`
FILE=`/bin/basename $7`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$SPKIR/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$SPKIR/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$SPKIR/$CFILE.coeff"
URL="https://raw.githubusercontent.com/ooi-integration/asset-management/master/calibration/$UID.csv"

# Process the file (if it hasn't already been done)
if [ -e $IN ] && [ ! -e $OUT ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_spkir -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT -cf $COEFF -u $URL
fi
