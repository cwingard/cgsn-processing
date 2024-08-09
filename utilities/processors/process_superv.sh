#!/bin/bash
#
# Read the parsed CPM SUPERV data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# C. Wingard 2017-01-24 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# check the processing flag for the correct supervisor type (CPM, DCL or STC)
case ${FLAG,,} in
    "cpm" | "stc" | "dcl" )
        ;;
    * )
        echo "ERROR: Incorrect supervisor type, $FLAG, in the processing"
        echo "flag. Please specify either CPM, DCL or STC for the type of"
        echo "supervisor log with the -f option."
        exit
        ;;
esac

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_superv -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -s ${FLAG,,} -i $IN_FILE -o $OUT_FILE || echo "ERROR: Failed to process $IN_FILE"
fi
