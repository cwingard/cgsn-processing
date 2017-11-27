#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude of the mooring,"
    echo "the DCL id, the deployment depth of the sensor, the subassembly [buoy/nsif/mfn] location, and the serial"
    echo "of the unit."
    echo "     example: $0 ce07shsm D00001 44.639 -124.304 dcl35 87 mfn C0120"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
DEPTH=$6
SUBASY=${7,,}
SERIAL=${8^^}

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw pco2w data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/pco2w*/*.log; do
    FNAME=`basename $file`
    DNAME=`dirname $file`
    DNAME=`basename $DNAME`
    echo "$FNAME"
    $PARSE/harvest_pco2w.sh $PLATFORM $DEPLOY $DCL $DNAME $SUBASY $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed pco2w data"
for file in $PROC/$PLATFORM/$DEPLOY/$SUBASY/pco2w/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LON "$SUBASY/pco2w" $DEPTH $SERIAL $FNAME
done
