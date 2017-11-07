#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce02shsm D00001 44.639 -124.304"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
DEPTH=$6
MFN=${7,,}

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw phsen data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/phsen*/*.log; do
    FNAME=`basename $file`
    foo=`dirname $file`
    DNAME=`basename $foo`
    echo "$FNAME"
    $PARSE/harvest_phsen.sh $PLATFORM $DEPLOY $DCL $DNAME $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed phsen data"
for file in $PROC/$PLATFORM/$DEPLOY/$MFN/phsen/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LON "$MFN/phsen" $DEPTH $FNAME
done

