#!/bin/bash
#
# Read the parsed CTDBP (includes DOSTA and FLORT) data files from the CGSN
# Global Surface Mooring Inductive Modem lines and create processed datasets
# available in NetCDF formatted files for further processing and review.
#
# C. Wingard 2019-10-18 -- Original script
# C. Wingard 2024-03-22 -- Updated to use the process_options.sh script to
#                          parse the command line inputs

# include the help function and parse the required and optional command line options
DIR="${BASH_SOURCE%/*}"
if [[ ! -d "$DIR" ]]; then DIR="$PWD"; fi
source "$DIR/process_options.sh"

# Split the serial number into the individual serial numbers for the DOSTA and FLORT
{
  IFS=';' read -r -a SERIALS <<< "$NSERIAL"
} || {
  echo "ERROR: Failed to split the DOSTA and FLORT serial numbers."
  echo "Please specify the two serial numbers, DOSTA first, as a single"
  echo "string separated by a semicolon, e.g. 1234;5678"
  exit
}
DOSTA_SERIAL=${SERIALS[0]}
FLORT_SERIAL=${SERIALS[1]}

# Process the file
if [ -e $IN_FILE ]; then
    cd /home/ooiuser/code/cgsn-processing || exit
    python -m cgsn_processing.process.proc_imm_ctdbp -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH \
      -i $IN_FILE -o $OUT_FILE -dsn $DOSTA_SERIAL -fsn $FLORT_SERIAL || echo "ERROR: Failed to process $IN_FILE"
fi
