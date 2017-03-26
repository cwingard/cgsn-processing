#!/bin/bash
#
# Read the parsed OPTAA data files from the Endurance Surface Moorings and 
# create processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied, rough temperature and salinity 
# corrections (for now) and an initial scatter correction for further 
# processing and review.
#
# C. Wingard 2017-01-23

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the OPTAA"
    echo "directory name, the UID name of the stored factory calibration data, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/optaa 7 OPTAAD/CGINS-OPTAAD-00208__20160921
    20161012_233000.optaa
    .json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
OPTAA=${5,,}
DEPTH=$6
UID=${7^^}
CFILE=`/bin/basename $UID`
FILE=`/bin/basename $8`

# Set the default directory paths and input/output sources
PYTHON="/home/cgsnmo/anaconda3/envs/ooi/bin/python"

DATA="/webdata/cgsn/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$OPTAA/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$OPTAA/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$OPTAA/$CFILE.coeff"
URL="https://github.com/ooi-integration/asset-management/raw/master/calibration/$UID.csv"

# Process the file (if it hasn't already been done)
if [ -e $IN ] && [ ! -e $OUT ]; then
    cd /home/cgsnmo/dev/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_optaa -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -s $DEPTH -i $IN -o $OUT -cf $COEFF -u $URL
fi
