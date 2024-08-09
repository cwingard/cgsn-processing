#!/bin/bash
#
# Read the parsed ADCP data files from the CGSN Global Surface Mooring
# Inductive Modem lines and create processed datasets available in
# NetCDF formatted files for further processing and review.
#
# C. Wingard 2023-03-03 -- Original code
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_imm_adcp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -sn $NSERIAL || echo "ERROR: Failed to process $IN_FILE"
fi
