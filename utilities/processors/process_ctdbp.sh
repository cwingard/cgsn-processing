#!/bin/bash
#
# Read the parsed CTDBP data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the CTDBP"
    echo " directory name, the deployment depth, the serial number of the DOSTA or FLORT (if applicable), a switch to"
    echo " indicate the configuration of the CTDBP (solo, dosta or flort) and the name of the file to process."
    echo ""
    echo "     example (SOLO): $0 ce07shsm D00004 44.63929 -124.30404 nsif/ctdbp 7 NaN solo 20161012.ctdbp1.json"
    echo "     example (DOSTA): $0 ce07shsm D00004 44.63929 -124.30404 mfn/ctdbp 87 477 dosta 20161012.ctdbp2.json"
    echo "     example (FLORT): $0 ce06issm D00005 44.63929 -124.30404 buoy/ctdbp 1 1154 flort 20161012.ctdbp3.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
CTDBP=${5,,}
DEPTH=$6
SERIAL=$7
SWITCH=$8
FILE=`basename $9`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/proc/$PLATFORM/$DEPLOY/$CTDBP/$FILE"
OUT="$DATA/erddap/$PLATFORM/$DEPLOY/$CTDBP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_ctdbp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -sn $SERIAL \
      -s $SWITCH -i $IN -o $OUT
fi
