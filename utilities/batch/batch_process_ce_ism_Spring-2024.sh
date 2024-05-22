#!/bin/bash -e
#
# Process the various data files for a Coastal Endurance Inshore Surface
# Mooring from the Spring 2024 Deployment (Endurance 20).
#
# Wingard, C. 2024-05-01 -- Initial version

# Parse the command line inputs
if [ $# -ne 2 ]; then
    echo "$0: required inputs are the platform and deployment name"
    echo "     example: $0 ce01issm D00020"
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
source /home/ooiuser/miniconda/bin/activate ooi

# Set some instrument names and processing flags based on the platform name
case "$PLATFORM" in
    "ce01issm"  )
        MFN_DEPTH=25
        LAT=44.659
        LON=-124.095
        FLR1="1151"
        FLR2="1154"
        PCO21="C0126"
        PCO22="C0061"
        PH1="P0167"
        PH2="P0072"
        ;;
    "ce06issm" )
        MFN_DEPTH=29
        LAT=47.133
        LON=-124.272
        FLR1="1211"
        FLR2="1303"
        PCO21="C0052"
        PCO22="C0062"
        PH1="P0168"
        PH2="P0085"
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

#### Buoy instruments ####
assembly="buoy"
depth=0
# control systems
$POLLING "$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly gps" "$PARSED/$assembly/gps/*.gps.json"
$POLLING "$PROCESS/process_syslog_irid.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly irid" "$PARSED/$assembly/irid/*.syslog.json"
$POLLING "$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly test" "$PARSED/$assembly/test/*.syslog.json"
$POLLING "$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/cpm1" "$PARSED/$assembly/superv/cpm1/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl17" "$PARSED/$assembly/superv/dcl17/*.superv.json"

# instruments
$POLLING "$PROCESS/process_ctdbp.sh -f flort -s $FLR1 $PLATFORM $DEPLOY $LAT $LON 1.5 $assembly ctdbp" "$PARSED/$assembly/ctdbp/*.ctdbp*.json"
$POLLING "$PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly mopak" "$PARSED/$assembly/mopak/*.mopak.json"
$POLLING "$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON 1.5 $assembly velpt" "$PARSED/$assembly/velpt/*.velpt*.json"

#### NSIF instruments ####
assembly="nsif"
depth=7
# control systems
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl16" "$PARSED/$assembly/superv/dcl16/*.superv.json"

# instruments
$POLLING "$PROCESS/process_ctdbp.sh -f dosta $PLATFORM $DEPLOY $LAT $LON $depth $assembly ctdbp" "$PARSED/$assembly/ctdbp/*.ctdbp*.json"
$POLLING "$PROCESS/process_flort.sh -c ctdbp1 -s $FLR2 $PLATFORM $DEPLOY $LAT $LON $depth $assembly flort" "$PARSED/$assembly/flort/*.flort.json"
$POLLING "$PROCESS/process_suna.sh -c ctdbp1 $PLATFORM $DEPLOY $LAT $LON $depth $assembly nutnr" "$PARSED/$assembly/nutnr/*.nutnr.json"
$POLLING "$PROCESS/process_optaa.sh -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly optaa" "$PARSED/$assembly/optaa/*.optaa*.json"
$POLLING "$PROCESS/process_pco2w.sh -s $PCO21 $PLATFORM $DEPLOY $LAT $LON $depth $assembly pco2w" "$PARSED/$assembly/pco2w/*.pco2w*.json"
$POLLING "$PROCESS/process_phsen.sh -c ctdbp -s $PH1 $PLATFORM $DEPLOY $LAT $LON $depth $assembly phsen" "$PARSED/$assembly/phsen/*.phsen*.json"
$POLLING "$PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly spkir" "$PARSED/$assembly/spkir/*.spkir.json"
$POLLING "$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly velpt" "$PARSED/$assembly/velpt/*.velpt*.json"

# MFN
assembly="mfn"
depth=$MFN_DEPTH
# control systems
$POLLING "$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/cpm3" "$PARSED/$assembly/superv/cpm3/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl36" "$PARSED/$assembly/superv/dcl36/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl37" "$PARSED/$assembly/superv/dcl37/*.superv.json"

# instruments
$POLLING "$PROCESS/process_ctdbp.sh -f dosta $PLATFORM $DEPLOY $LAT $LON $depth $assembly ctdbp" "$PARSED/$assembly/ctdbp/*.ctdbp*.json"
$POLLING "$PROCESS/process_adcp.sh -f pd0 -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly adcp" "$PARSED/$assembly/adcp/*.adcp*.json"
$POLLING "$PROCESS/process_optaa.sh -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly optaa" "$PARSED/$assembly/optaa/*.optaa*.json"
$POLLING "$PROCESS/process_pco2w.sh -s $PCO22 $PLATFORM $DEPLOY $LAT $LON $depth $assembly pco2w" "$PARSED/$assembly/pco2w/*.pco2w*.json"
$POLLING "$PROCESS/process_phsen.sh -c ctdbp -s $PH2 $PLATFORM $DEPLOY $LAT $LON $depth $assembly phsen" "$PARSED/$assembly/phsen/*.phsen*.json"
$POLLING "$PROCESS/process_presf.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly presf" "$PARSED/$assembly/presf/*.presf.json"
#$POLLING "$PROCESS/process_vel3d.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly vel3d" "$PARSED/$assembly/vel3d/*.vel3d.json"
$POLLING "$PROCESS/process_zplsc.sh -f 2.004 $PLATFORM $DEPLOY $LAT $LON $depth $assembly zplsc" "$PARSED/$assembly/zplsc/*.zplsc.json"
