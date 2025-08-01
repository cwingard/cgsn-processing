#!/bin/bash
#
# Read the parsed SPKIR data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files with the vendor
# factory calibration coefficients applied for further processing and review.
#
# C. Wingard 2017-01-23 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# Process the file (if it hasn't already been done)
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_spkir -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -ba || echo "ERROR: Failed to process $IN_FILE"
fi
