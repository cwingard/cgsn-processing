#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude of the mooring,"
    echo "the DCL id, the deployment depth of the sensor, the subassembly [buoy/nsif/mfn] location, and the name"
    echo "of the co-located CTD."
    echo "     example: $0 ce01issm D00008 44.639 -124.304 dcl16 7 nsif ctdbp1"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
DEPTH=$6
SUBASY=$7
CTD=${8,,}

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw suna data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/nutnr*/*.log; do
    FNAME=`basename $file`
    DNAME=`dirname $file`
    DNAME=`basename $DNAME`
    echo "$FNAME"
    $PARSE/harvest_suna.sh $PLATFORM $DEPLOY $DCL $DNAME $SUBASY $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed suna data"
for file in $PROC/$PLATFORM/$DEPLOY/$SUBASY/nutnr/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_suna.sh $PLATFORM $DEPLOY $LAT $LON "$SUBASY/nutnr" $CTD $DEPTH $FNAME
done
