#!/bin/bash
#
# Read the parsed Prawler MMP data files from the CGSN Shallow Water Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# P. Whelan 2024-05-08 -- Original script
# C. Wingard 2024-05-12 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_mmp_prawler -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE || echo "ERROR: Failed to process $IN_FILE"
fi
