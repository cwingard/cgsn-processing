#!/bin/bash
#
# Read the parsed CTDBP data files from the CGSN Coastal Surface Moorings and
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

# check the processing flag used to add processing for optional additional sensors (solo, dosta, flort)
case $FLAG in
    "solo" | "dosta" | "flort" )
        ;;
    * )
        echo "ERROR: Incorrect CTDBP data contents name, $FLAG, in the"
        echo "processing flag. Please specify either solo, dosta, or flort"
        echo "(case-insensitive) to indicate the contents of the CTDBP data"
        echo "file with the -f option."
        exit
        ;;
esac

# check that the serial number is provided (FLORT only), if not set to default value of None
if [ "$FLAG" == "flort" ]; then
    if [ -z "$NSERIAL" ]; then
        echo "ERROR: The serial number for the FLORT sensor must be provided with the -s option."
        exit
    fi
else
    NSERIAL="None"
fi

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_ctdbp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -s $FLAG -sn $NSERIAL || echo "ERROR: Failed to process $IN_FILE"
fi
