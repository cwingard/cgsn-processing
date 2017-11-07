#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 4 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce02shsm D00001 44.639 -124.304"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw FB250 data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/syslog/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_syslog_fb250.sh $PLATFORM $DEPLOY $FNAME
done

echo "Processing $PLATFORM/$DEPLOY parsed FB250 data"
for file in $PROC/$PLATFORM/$DEPLOY/buoy/fb250/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_syslog_fb250.sh $PLATFORM $DEPLOY $LAT $LON "buoy/fb250" $FNAME
done
