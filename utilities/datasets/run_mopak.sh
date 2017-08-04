#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 5 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce09ossm D00001 46.851 -124.972"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
DCL=$3
LAT=$4
LNG=$5


# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Process the files
echo "Processing $PLATFORM/$DEPLOY raw mopak data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/mopak/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_mopak.sh $PLATFORM $DEPLOY $DCL $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed mopak data"
for file in $PROC/$PLATFORM/$DEPLOY/buoy/mopak/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/mopak" $FNAME
done
