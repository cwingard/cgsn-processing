#!/bin/bash
#
# Read the parsed RBR/Q3 data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files.
#
# P. Whelan 2023-12-06 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs
# P. Whelan  2024-09-19 -- Revised to use Q3 specific processor

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_rbrpresf -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE || echo "ERROR: Failed to process $IN_FILE"
fi
