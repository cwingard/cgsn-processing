#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 5 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "the DCL name, the calibration file name and the latitude and longitude"
    echo "     example: $0 ce02shsm D00005 dcl26 44.639 -124.304"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
DCL=$3
LAT=$4
LON=$5

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw spkir data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/spkir/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_spkir.sh $PLATFORM $DEPLOY $DCL spkir nsif $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed spkir data"
for file in $PROC/$PLATFORM/$DEPLOY/nsif/spkir/*.json; do
    FNAME=`basename "$file"`
    echo "$FNAME"
    $PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LON "nsif/spkir" 7 $FNAME
done
