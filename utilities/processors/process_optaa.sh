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
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the OPTAA"
    echo "directory name, the UID name of the stored factory calibration data,"
    echo "and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 nsif/optaa OPTAAD/CGINS-OPTAAD-00208__20160921 20161012_233000.optaa.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
OPTAA=${5,,}
UID=${6^^}
CFILE=`/bin/basename $UID`
FILE=`/bin/basename $7`

# Set the default directory paths and input/output sources
BIN="/home/cgsnmo/dev/cgsn-processing/cgsn_processing/process"
PYTHON="/home/cgsnmo/anaconda3/envs/py27/bin/python"

DATA="/webdata/cgsn/data/proc"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$OPTAA/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$OPTAA/${FILE%.json}.nc"

COEFF="$PROC/$PLATFORM/$DEPLOY/$OPTAA/$CFILE.coeff"
URL="https://github.com/ooi-integration/asset-management/raw/master/calibration/$UID.csv"

# Process the file (if it hasn't already been done)
if [ -e $IN ] && [ ! -e $OUT ]; then
    $PYTHON -m $BIN/proc_optaa -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT -cf $COEFF -u $URL
fi
