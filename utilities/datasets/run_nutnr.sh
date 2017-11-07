#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the DCL used,"
    echo "the latitude and longitude, the name of the co-located CTD, the deployment"
    echo "depth, a switch to indicate presence/absence of the full spectra, and the"
    echo "name of the file to process."
    echo "     example: $0 ce02shsm D00001 44.639 -124.304 ctdbp 7 1"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DCL=${5,,}
CTD=${6,,}
DEPTH=$7
SWITCH=$8

# Set the default directory paths
RAW="/home/ooiuser/data/raw"
PARSE="/home/ooiuser/code/cgsn-parsers/utilities/harvesters"
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Parse the files
echo "Parsing $PLATFORM/$DEPLOY raw nutnr data"
for file in $RAW/$PLATFORM/$DEPLOY/cg_data/$DCL/nutnr/*.log; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PARSE/harvest_nutnr.sh $PLATFORM $DEPLOY $DCL nutnr nsif $SWITCH $FNAME
done

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed nutnr data"
for file in $PROC/$PLATFORM/$DEPLOY/nsif/nutnr/*.json; do
    FNAME=`basename $file`
    echo "$FNAME"
    $PROCESS/process_nutnr.sh $PLATFORM $DEPLOY $LAT $LON "nsif/nutnr" $CTD $DEPTH $SWITCH $FNAME
done
