#!/bin/bash
#
# Read the parsed PCO2W data files from the CGSN Coastal Surface Moorings and create
# processed datasets available in JSON formatted files with the vendor factory
# calibration coefficients applied for further processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the PCO2W directory"
    echo "name, the deployment depth, the unit serial number, and the name of the file to process."
    echo ""
    echo "     example: $0 ce07shsm D00004 46.98589 -124.56490 mfn/pco2w 87 C0082 20161012.pco2w.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
PCO2W=${5,,}
DEPTH=$6
SERIAL=${7^^}
FILE=`basename $8`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$PCO2W/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$PCO2W/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$PCO2W/pco2w_factory_calibration.coeffs"
BLANK="$DATA/proc/$PLATFORM/$DEPLOY/$PCO2W/pco2w_factory_calibration.blanks"

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_pco2w -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -i $IN -o $OUT -cf $COEFF -df $BLANK -sn $SERIAL
fi
