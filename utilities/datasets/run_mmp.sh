#!/bin/bash -e

# Parse the command line inputs
if [ $# -ne 2 ]; then
    echo "$0: required inputs are the platform and deployment names,"
    echo "in that order, and the name of the file to process."
    echo "     example: $0 ce09ospm D00001"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}

# Set the default directory paths
PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Process the files
echo "Processing $PLATFORM/$DEPLOY parsed and collated profiler data"
for mmp in $PROC/$PLATFORM/$DEPLOY/imm/mmp/P*.json; do
    SIZE=`du -k "$mmp" | cut -f1`
    if [ $SIZE > 0 ]; then
	echo $mmp
        $PROCESS/process_mmp_coastal.sh $PLATFORM $DEPLOY 46.852 -124.975 "imm/mmp" $mmp
    fi
done

