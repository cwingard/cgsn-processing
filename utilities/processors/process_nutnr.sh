#!/bin/bash
#
# Read the parsed NUTNR data files from the CGSN Coastal Surface Moorings and
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

# check the processing flag for the correct ISUS data record type (full or condensed)
case $FLAG in
    0 | 1 )
        ;;
    * )
        echo "ERROR: Incorrect ISUS record type, $FLAG, in the processing"
        echo "flag. Please specify either 0 (condensed) or 1 (full) for the"
        echo "the ISUS data record format with the -f option."
        exit
        ;;
esac

# check that the co-located CTD name is provided
if [ -z "$COLOCATED" ]; then
    echo "ERROR: The co-located CTD name must be provided with the -c option."
    exit
fi

# set the name of the calibration coefficients file
COEFF="$(dirname "$IN_FILE")/nutnr.cal_coeffs.json"

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_nutnr -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -s $FLAG -df $COLOCATED -cf $COEFF || echo "ERROR: Failed to process $IN_FILE"
fi
