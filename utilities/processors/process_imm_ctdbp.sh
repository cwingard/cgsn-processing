#!/bin/bash
#
# Read the parsed CTDBP (includes DOSTA and FLORT) data files from the CGSN
# Global Surface Mooring Inductive Modem lines and create processed datasets
# available in NetCDF formatted files for further processing and review.
#
# C. Wingard 2019-10-18

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the CTDBP"
    echo " directory name, the deployment depth, the serial numbers of the DOSTA and FLORT, and the name"
    echo " of the file to process."
    echo ""
    echo "     example: $0 gi01sumo D00004 59.9462 -39.4737 imm/ctdbp 40 498 3417 ctdbp01_20171010_111822.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
CTDBP=${5,,}
DEPTH=$6
oxy_serial=$7
flr_serial=$8
FILE=`basename $9`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$CTDBP/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$CTDBP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing
    python -m cgsn_processing.process.proc_imm_ctdbp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -dsn $oxy_serial -fsn $flr_serial -i $IN -o $OUT
fi
