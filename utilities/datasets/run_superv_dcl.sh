#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce09ossm D00001 dcl26 nsif/superv/dcl26 46.851 -124.972"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
DCL=$3
OUT=$4
LAT=$5
LON=$6


# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Process the files
echo "Processing $PLATFORM/$DEPLOY raw $DCL supervisor data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/superv/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_superv_dcl.sh $PLATFORM $DEPLOY $DCL $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed supervisor data"
for file in $PROC/$PLATFORM/$DEPLOY/$OUT/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $OUT $FNAME
done
