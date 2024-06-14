#!/bin/bash -e
#
# Process the various data files for a Coastal Endurance Profiler Mooring.
#
# Wingard, C. 2024-05-02 -- Initial version

# Parse the command line inputs
if [ $# -ne 2 ]; then
    echo "$0: required inputs are the platform and deployment name"
    echo "     example: $0 ce09ospm D00020"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}

# set the directory paths for the parsed data files and the processing scripts
PARSED="/home/ooiuser/data/parsed/$PLATFORM/$DEPLOY"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# set the polling script name and absolute path
POLLING="/home/ooiuser/code/cgsn-parsers/utilities/harvesters/polling.sh"

# load the ooi python environment
source /home/ooiuser/miniconda/bin/activate ooi-old

# set a default position for the platform (center of the PATON permit area)
LAT="46.851"
LON="-124.972"

#### Buoy instruments ####
assembly="buoy"
depth=0
# control systems
$POLLING "$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly gps" "$PARSED/$assembly/gps/*.syslog.json"
$POLLING "$PROCESS/process_syslog_irid.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly irid" "$PARSED/$assembly/irid/*.syslog.json"
$POLLING "$PROCESS/process_superv_stc.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv" "$PARSED/$assembly/superv/*.syslog.json"
# instruments
$POLLING "$PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly mopak" "$PARSED/$assembly/mopak/*.3dmgx3.json"

#### IMM/MMP Instruments ####
assembly="imm"
depth=542
# MMP profiles
$POLLING "$PROCESS/process_mmp_coastal.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly mmp" "$PARSED/$assembly/mmp/P000*.json"
