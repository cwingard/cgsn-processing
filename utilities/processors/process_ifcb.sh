#!/bin/bash
#
# Read the parsed IFCB data files from the CGSN Coastal Surface Moorings and
# create processed datasets available in NetCDF formatted files for further
# processing and review.
#
# P. Whelan 2023-12-06 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# check the processing flag for the correct ADCP data types (PD0 or PD8)
case $FLAG in
    "adc" | "hdr" )
        ;;
    * )
        echo "ERROR: Incorrect IFCB data file type, $FLAG, in the processing"
        echo "flag. Please specify either ADC or HDR (case-insensitive) for"
        echo "the data record type with the -f option."
        exit
        ;;
esac

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_ifcb -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -s $FLAG || echo "ERROR: Failed to process $IN_FILE"
fi
