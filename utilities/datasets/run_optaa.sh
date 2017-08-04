#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude,"
    echo "the DCL name, the sensor depth, and the subplatform name, in that order."
    echo "     example: $0 ce07shsm D00001 44.639 -124.304 dcl37 87 mfn"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LNG=$4
DCL=${5,,}
DEPTH=$6
SUB=${7,,}

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw optaa data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/optaa*/*.log; do
    FNAME=`basename $file`
    foo=`dirname $file`
    DNAME=`basename $foo`
    echo "$FNAME"
    $PARSE/harvest_optaa.sh $PLATFORM $DEPLOY $DCL $DNAME $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed optaa data"
for file in $PROC/$PLATFORM/$DEPLOY/$SUB/optaa/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "$SUB/optaa" $DEPTH $FNAME
done

