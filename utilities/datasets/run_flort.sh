#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude of the mooring,"
    echo "the DCL id, the deployment depth of the sensor, the subassembly [buoy/nsif/mfn] location, the serial number"
    echo "of the unit, and the directory name of the co-located CTD."
    echo "     example: $0 ce02shsm D00001 44.639 -124.304 dcl27 7 nsif 1123 ctdbp"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
DEPTH=$6
SUBASY=${7,,}
SERIAL=$8
CTD=${9,,}

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw flort data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/flort*/*.log; do
    FNAME=`basename $file`
    DNAME=`dirname $file`
    DNAME=`basename $DNAME`
    echo "$FNAME"
    $PARSE/harvest_flort.sh $PLATFORM $DEPLOY $DCL $DNAME $SUBASY $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed flort data"
for file in $PROC/$PLATFORM/$DEPLOY/$SUBASY/flort/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LON "$SUBASY/flort" $CTD $DEPTH $SERIAL $FNAME
done

