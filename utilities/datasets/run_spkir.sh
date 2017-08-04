#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "the DCL name, the calibration file name and the latitude and longitude"
    echo "     example: $0 ce02shsm D00005 dcl26 CE02SHSM_D00005_SPKIR.coeff 44.639 -124.304"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
DCL=$3
COEFF=$4
LAT=$5
LNG=$6

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
#echo "Parsing $PLATFORM/$DEPLOY raw spkir data"
#for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/spkir/*.log; do
#    FNAME=`basename $file`
#    echo "$FNAME"
#    $PARSE/harvest_spkir.sh $PLATFORM $DEPLOY $DCL $FNAME
#done

echo "Processing $PLATFORM/$DEPLOY parsed spkir data"
files=($PROC/$PLATFORM/$DEPLOY/nsif/spkir/*.json)
for ((i=${#files[@]}-1; i>=0; i--)) do
    FNAME=`basename "${files[$i]}"`
    echo "$FNAME"
    $PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/spkir" $COEFF $FNAME || echo "$FNAME processing failed"
done


