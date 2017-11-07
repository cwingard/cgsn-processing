#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude "
    echo "and longitude of the mooring, DCL name, deployment depth, and the ctd"
    echo "location and type"
    echo "     example: $0 ce02shsm D00001 44.639 -124.304 dcl27 7 buoy 1"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
DEPTH=$6
LOCATE=${7,,}
TYPE=$8

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw ctdbp data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/ctdbp*/*.log; do
    FNAME=`basename $file`
    PNAME=`dirname $file`
    DNAME=`basename $PNAME`
    echo "$FNAME"
    $PARSE/harvest_ctdbp.sh $PLATFORM $DEPLOY $DCL $DNAME $LOCATE $TYPE $FNAME 
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed ctdbp data"
for file in $PROC/$PLATFORM/$DEPLOY/$LOCATE/ctdbp/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LON "$LOCATE/ctdbp" $DEPTH $FNAME
done

