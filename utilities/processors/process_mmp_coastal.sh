#!/bin/bash
#
# Read the parsed Coastal MMP data files from the Profiler Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 10 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude"
    echo "and longitude, the MMP directory name, the deployment depth, the serial"
    echo "numbers of the DOFST, FLORT and PARAD sensors, and the name of the file"
    echo "to process."
    echo ""
    echo "     example: $0 ce09ospm D00006 46.85165 -124.98229 imm/mmp 542 2498 1032 20448 P0000125.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
MMP=${5,,}
DEPTH=$6
OXY_SERIAL=$7
FLR_SERIAL=$8
PAR_SERIAL=$9
FILE=`basename $10`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$MMP/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$MMP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the profiler dataset
if [ -e $IN ] && [ ! -e ${OUT%.nc}_edata.nc ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_mmp_coastal -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -dsn $oxy_serial -fsn $flr_serial -psn $par_serial -i $IN -o $OUT
fi
