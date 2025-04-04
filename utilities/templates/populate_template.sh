#!/bin/bash
#
# Use the populate_template.sh script to create a new YAML configuration file
# for a mooring deployment. The script will use the specified mooring and
# deployment number to create the new file based on the specified template
# source file.
#
# C. Wingard 2025-04-02 -- Original script

# Then parse the required command line inputs and check the number of inputs
if [ $# -ne 4 ]; then
  echo "Error: Incorrect number of inputs. Please specify the platform name, deployment"
  echo "name, the template file to use and the name (with path information if desired) of"
  echo "the new file to create."
  echo ""
  exit
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
TEMPLATE_FILE=$3
OUT_FILE=$4

# Process the file
if [ -e "$TEMPLATE_FILE" ]; then
  cd "$HOME/code/cgsn-processing" || exit
  python -m cgsn_processing.process.templates.generate_yaml -m "$PLATFORM" -d "$DEPLOY" -t "$TEMPLATE_FILE" \
    -o "$OUT_FILE" || echo "ERROR: Failed to create $OUT_FILE"
fi
