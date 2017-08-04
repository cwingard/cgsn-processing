#!/bin/bash

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and "
    echo "longitude of the mooring, site depth, and the FLORT and PARAD serial numbers"
    echo ""
    echo "     example: $0 ce01issp D00007 44.659 -124.095 25 1518 504"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LNG=$4
DEPTH=$5
FLORT=$6
PARAD=$7

PARSE="/home/ooiuser/code/cgsn-parsers"
PROCESS="/home/ooiuser/code/cgsn-processing"

# convert the raw data files to JSON
cd $PARSE
./utilities/harvesters/master_harvester_ucspp.sh $PLATFORM $DEPLOY PPD

# now convert the parsed data files to netCDF file for use in ERDDAP
cd $PROCESS
./utilities/processors/process_ucspp.sh $PLATFORM $DEPLOY $LAT $LNG $DEPTH PPD $FLORT $PARAD 0
