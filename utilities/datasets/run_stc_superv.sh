#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 4 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce09ospm D00001 46.851 -124.972"
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
echo "Parsing $PLATFORM/$DEPLOY raw Supervisor data"
for file in $RAW/$PLATFORM/$DEPLOY/syslog/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_superv_stc.sh $PLATFORM $DEPLOY $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed supervisor data"
for file in $PROC/$PLATFORM/$DEPLOY/buoy/superv/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_superv_stc.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv" $FNAME
done

