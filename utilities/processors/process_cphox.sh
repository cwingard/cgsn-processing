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
# C. Wingard 2025-01-24 -- Updated to use the estimated alkalinity flag to
#                          determine if the processor should add estimated
#                          total alkalinity values to the data set.

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# check the platform name and set the processing flag to add estimations of the
# total alkalinity to the data set.
case $FLAG in
    "estimate" )
        ;;
    * )
        echo "ERROR: Incorrect SeapHOx processing flag, $FLAG, Please use"
        echo "'estimate' to indicate the processor should add estimated"
        echo "alkalinity values with the -f option. Otherwise, do not use"
        echo "this option."
        exit
        ;;
esac

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_cphox -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -s $FLAG || echo "ERROR: Failed to process $IN_FILE"
fi
