#!/bin/bash

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and "
    echo "longitude of the mooring, site depth, and the FLORT, PARAD and NUTNR serial numbers"
    echo ""
    echo "     example: $0 ce01issp R00001 44.659 -124.095 25 1084 365 337"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DEPTH=$5
FLORT=$6
PARAD=$7
NUTNR=$8

PARSE="/home/ooiuser/code/cgsn-parsers"
PROCESS="/home/ooiuser/code/cgsn-processing"

# convert the raw data files to JSON
cd $PARSE
./utilities/harvesters/master_harvester_ucspp.sh $PLATFORM $DEPLOY PPB
./utilities/harvesters/master_harvester_ucspp.sh $PLATFORM $DEPLOY SNA
./utilities/harvesters/master_harvester_ucspp.sh $PLATFORM $DEPLOY ACS
./utilities/harvesters/master_harvester_ucspp.sh $PLATFORM $DEPLOY WC

# now convert the parsed data files to netCDF file for use in ERDDAP
cd $PROCESS
./utilities/processors/process_ucspp.sh $PLATFORM $DEPLOY $LAT $LON $DEPTH PPB $FLORT $PARAD 0
./utilities/processors/process_ucspp.sh $PLATFORM $DEPLOY $LAT $LON $DEPTH SNA 0 0 $NUTNR
./utilities/processors/process_ucspp.sh $PLATFORM $DEPLOY $LAT $LON $DEPTH ACS 0 0 0
./utilities/processors/process_ucspp.sh $PLATFORM $DEPLOY $LAT $LON $DEPTH WC 0 0 0
