#!/bin/bash
#
# Read the parsed PCO2W data files from the Endurance Surface Moorings and create
# processed datasets available in JSON formatted files with the vendor factory
# calibration coefficients applied for further processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the PCO2W"
    echo "directory name, the UNIQUE_ID name of the stored factory calibration data,"
    echo "and the name of the file to process."
    echo ""
    echo "     example: $0 ce07shsm D00004 mfn/pco2w PCO2WB/CGINS-PCO2WB-C0082__20160921 20161012.pco2w.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
PCO2W=${5,,}
UNIQUE_ID=${6^^}
CFILE=`/bin/basename $UNIQUE_ID`
FILE=`/bin/basename $7`

# Set the default directory paths and input/output sources
BIN="/home/ooiuser/code/cgsn-processing/cgsn_processing/process"
PYTHON="/home/cgsnmo/anaconda3/envs/py27/bin/python"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$PCO2W/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$PCO2W/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/erddap/$PLATFORM/$DEPLOY/$PCO2W/$CFILE.coeff"
BLANK="$DATA/erddap/$PLATFORM/$DEPLOY/$PCO2W/$CFILE.blank"
URL="https://github.com/ooi-integration/asset-management/raw/master/calibration/$UNIQUE_ID.csv"

# Process the file
if [ -e $IN ]; then
    $PYTHON -m $BIN/proc_pco2w -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -i $IN -o $OUT -cf $COEFF -df $BLANK -u $URL
fi
