#!/bin/bash
#
# Read the parsed ADCP data files from the CGSN Global Surface Mooring
# Inductive Modem lines and create processed datasets available in
# NetCDF formatted files for further processing and review.
#
# C. Wingard 2023-03-03

# Parse the command line inputs
if [ $# -ne 8 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and longitude, the ADCP"
    echo " directory name, the ADCP serial number, the deployment depth, and the name of the file to process."
    echo ""
    echo "     example: $0 gi01sumo D0009 59.9462 -39.4737 imm/adcp 500 18000 20230303_122800.adcpt.json"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3; LON=$4
ADCP=${5,,}
DEPTH=$6
SERIAL=$7
FILE=`basename $8`

# Set the default directory paths and input/output sources
DATA="/home/ooiuser/data"
IN="$DATA/parsed/$PLATFORM/$DEPLOY/$ADCP/$FILE"
OUT="$DATA/processed/$PLATFORM/$DEPLOY/$ADCP/${FILE%.json}.nc"
if [ ! -d `dirname $OUT` ]; then
    mkdir -p `dirname $OUT`
fi

# set the default name of the calibration coefficients file
COEFFS="$DATA/parsed/$PLATFORM/$DEPLOY/$ADCP/adcp.configuration.json"

# Process the file
if [ -e $IN ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_imm_adcp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -sn $SERIAL -cf $COEFFS -i $IN -o $OUT
fi
