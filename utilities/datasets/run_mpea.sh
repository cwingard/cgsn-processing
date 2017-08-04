#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 4 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce09ossm D00001 46.851 -124.972"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LNG=$4

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Process the files
echo "Processing $PLATFORM/$DEPLOY raw MPEA data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/cpm3/pwrsys/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_mpea.sh $PLATFORM $DEPLOY $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed MPEA data"
for file in $PROC/$PLATFORM/$DEPLOY/mfn/mpea/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_mpea.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/mpea" $FNAME
done
