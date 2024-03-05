#!/bin/bash
#
# Read the parsed CTDMO data files from the CGSN Global Surface Mooring
# Inductive Modem lines and create processed datasets available in NetCDF
# formatted files for further processing and review.
#
# C. Wingard 2023-04-14

# Parse the command line inputs
if [ $# -ne 7 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the CTDMO"
    echo " directory name, the deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 gi01sumo D0004 59.9462 -39.4737 imm/ctdmo01 ctdmo01_20171010_111822.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
CTDMO=${5,,}
DEPTH=$6
FILE=`basename $7`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$CTDMO/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$CTDMO/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_imm_ctdmo -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
        -i $IN -o $OUT
fi
