#!/bin/bash -e
#
# Parse the various data files for a Coastal Profiler Mooring.
#
# Wingard, C. 2017-04-07

# Parse the command line inputs
if [ $# -ne 3 ]; then
    echo "$0: required inputs are the platform and deployment name, and"
    echo "the time flag for processing today's file (0) or N days prior"
    echo "     example: $0 ce09ospm D00001 0"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
TIME="-$3 day"
FNAME=`/bin/date -u +%Y%m%d --date="$TIME"`

PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

LAT="46.85165"
LNG="-124.98229"

# Buoy
#$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/gps" $FNAME.gps.json
for mopak in $PROC/$PLATFORM/$DEPLOY/buoy/3dmgx3/$FNAME*.3dmgx3.json; do
    if [ -e $mopak ]; then
        SIZE=`du -k "$mopak" | cut -f1`
        if [ $SIZE > 0 ]; then
            $PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/3dmgx3" $mopak
        fi
    fi
done
$PROCESS/process_superv_stc.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv" $FNAME.syslog.json

# IMM/MMP
for mmp in $PROC/$PLATFORM/$DEPLOY/imm/mmp/P*.json; do
    SIZE=`du -k "$mmp" | cut -f1`
    if [ $SIZE > 0 ]; then
        $PROCESS/process_mmp_coastal.sh $PLATFORM $DEPLOY $LAT $LNG "imm/mmp" $mmp
    fi
done

# IMM/ADCPS
# <Add adcps processing here>
