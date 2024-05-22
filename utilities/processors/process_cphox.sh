#!/bin/bash
#
# Read the parsed Sea-Bird Electronics Deep SeapHOx V2 data files from the CGSN
# Coastal Surface Moorings and create processed datasets available in NetCDF
# formatted files for further processing and review.
#
# C. Wingard 2024-02-20 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs
# C. Wingard 2024-05-17 -- Updated to add the processing flag to indicate if
#                          the processor should add estimated calculations of
#                          the total alkalinity and pH to the output file.

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# check the platform name and set the processing flag to add estimations of the pH
# and total alkalinity to the data set (currently only available for the CE02SHSM
# platform).
case $PLATFORM in
    "CE02SHSM" )
        FLAG="estimate" ;;
    * )
        FLAG="none";;
esac

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_cphox -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -s $FLAG || echo "ERROR: Failed to process $IN_FILE"
fi
