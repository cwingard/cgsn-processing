#!/bin/bash
#
# Read the parsed RDA data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 6 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the RDA"
    echo " directory name, and the name of the file to process."
    echo ""
    echo "     example: $0 ce02shsm D00004 44.63929 -124.30404 buoy/rda 20161012.syslog.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
RDA=${5,,}
FILE=`basename $6`

# Set the default directory paths and input/output sources

DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$RDA/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$RDA/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_syslog_rda -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -i $IN -o $OUT
fi
