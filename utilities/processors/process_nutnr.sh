#!/bin/bash
#
# Read the parsed NUTNR data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the NUTNR"
    echo " directory name, the deployment depth, a switch to indicate absence/presence of the full wavelength array"
    echo "and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 nsif/nutnr 7 1 20161012.nutnr.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LNG=$4
NUTNR=${5,,}
DEPTH=$6
SWITCH=$7
FILE=`/bin/basename $8`

# Set the default directory paths and input/output sources
PYTHON="/home/ooiuser/bin/conda/bin/python3"

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$NUTNR/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$NUTNR/${FILE%.json}.nc"
if [ ! -d `/usr/bin/dirname $OUT` ]; then
    mkdir -p `/usr/bin/dirname $OUT`
fi

COEFF="$DATA/proc/$PLATFORM/$DEPLOY/$NUTNR/nutnr_factory_calibration.coeffs"

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    $PYTHON -m cgsn_processing.process.proc_nutnr -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LNG -dp $DEPTH -i $IN -o $OUT -cf $COEFF -s $SWITCH
fi
