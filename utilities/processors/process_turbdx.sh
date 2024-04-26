#!/bin/bash
#
# Read the parsed FLORT data files from the CGSN Coastal Surface Moorings and
# create TURBDX processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied for further processing and review.
#
# P. Whelan 2024-02-08
# C. Wingard 2024-04-26 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# check that the co-located CTD name is provided
if [ -z "$COLOCATED" ]; then
    echo "ERROR: The co-located CTD name must be provided with the -c option."
    exit
fi

# check that the serial number is provided
if [ -z "$NSERIAL" ]; then
    echo "ERROR: The TURBDX (aka FLORT) serial number must be provided with the -s option."
    exit
fi

# set the name of the calibration coefficients file
COEFF="$(dirname "$IN_FILE")/turbdx.cal_coeffs.json"

# Process the file (if it hasn't already been done)
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_flort -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
        -i $IN_FILE -o $OUT_FILE -sn $NSERIAL -df $COLOCATED -ba -cf $COEFF \
        -s TURBDX || echo "ERROR: Failed to process $IN_FILE"
fi
