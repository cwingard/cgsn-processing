#!/bin/bash
# process_options.sh
#
# This script is used to parse the command line inputs for the processors and
# provide a help function to display the required and optional inputs for the
# processor scripts.
#
# C. Wingard 2024-03-22 -- Original code

# create a function to print the help documentation
function help ()
{
  echo "$0: required inputs are the platform, deployment, latitude, longitude,"
  echo "depth and subassembly and instrument name, in that order, followed by"
  echo "the name of the file to process. Three optional flags can be set as"
  echo "defined below:"
  echo ""
  echo "Syntax: $0 [OPTIONS] platform deployment latitude longitude depth instrument file"
  echo ""
  echo "Options:"
  echo "h    Print this help message and exit."
  echo "f    Value of the processing flag, if used. Value is processor specific,"
  echo "     can be either a string, integer or float (optional)."
  echo "c    Name of a co-located instrument needed for the processing. Usually"
  echo "     this is the name of a co-located CTD (optional)."
  echo "s    Serial number of the instrument needed for the processing. This"
  echo "     number is used to look-up calibration coefficients needed to"
  echo "     convert values from raw units (e.g. counts) to engineering units"
  echo "     (e.g. mg/L) (optional)."
  echo ""
  echo "The inputs set the directory structure for where the processed data"
  echo "files are stored as well as adding required metadata. The file name"
  echo "is the name of the file to process (either relative or full path"
  echo "information is required). Note, the instrument name can include"
  echo "relative path information, if needed. For example, the instrument"
  echo "name could be specified as 'superv/dcl12' to indicate the processed"
  echo "data would be located in the 'superv/dcl12' directory."
  echo ""
  echo "Example: $0 ce02shsm D00017 44.639 -124.304 1 buoy superv/dcl12 20240202.superv.json"
}

# First parse the optional command line inputs
while getopts "hf:c:s:" option; do
  case $option in
    h ) # display Help
      help
      exit ;;
    f ) # Processing flag
      FLAG=${OPTARG,,} ;;
    c ) # Co-located instrument name
      COLOCATED=${OPTARG,,} ;;
    s ) # Serial number of the instrument
      NSERIAL=${OPTARG,,} ;;
    : )
      echo "Option -${OPTARG} requires an argument"
      exit ;;
    * ) # Invalid option
      echo "Error: Invalid option -${OPTARG}"
      exit ;;
  esac
done
shift $((OPTIND - 1))

# Then parse the required command line inputs and check the number of inputs
if [ $# -ne 8 ]; then
  echo "Error: Incorrect number of inputs. Please specify the platform name, deployment"
  echo "name, latitude, longitude, depth, subassembly name, instrument name and the"
  echo "file to parse, in that order."
  echo ""
  exit
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=${3}
LON=${4}
DEPTH=${5}
ASSMBLY=${6,,}
INSTRMT=${7,,}
IN_FILE=${8}
FNAME=$(basename "$IN_FILE")

# test that the input file exists and is not empty
if [ ! -s "$IN_FILE" ]; then
  echo "ERROR: The input file $IN_FILE does not exist or is empty."
  exit
fi

# Set the processed output data directory
PROCESSED="/home/ooiuser/data/processed"
OUT_DIR="$PROCESSED/$PLATFORM/$DEPLOY/$ASSMBLY/$INSTRMT"
OUT_FILE="$OUT_DIR/${FNAME%.json}.nc"
if [ ! -d "$OUT_DIR" ]; then
    mkdir -p "$OUT_DIR"
fi
