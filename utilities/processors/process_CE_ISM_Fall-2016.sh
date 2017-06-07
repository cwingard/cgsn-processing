#!/bin/bash -e
#
# Parse the various data files for a Coastal Surface Mooring.
#
# Wingard, C. 2015-04-17

# Parse the command line inputs
if [ $# -ne 3 ]; then
    echo "$0: required inputs are the platform and deployment name, and"
    echo "the time flag for processing today's file (0) or N days prior"
    echo "     example: $0 ce02shsm D00001 0"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
TIME="-$3 day"
FNAME=`/bin/date -u +%Y%m%d --date="$TIME"`

PROC="/home/ooiuser/data/proc"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# Set some instrument names and processing flags based on the platform name
case "$PLATFORM" in
    "ce01issm"  )
        MFN_FLAG=1
        MFN_DEPTH=25
        LAT=44.659
        LNG=-124.095
        declare -a FLORT=("FLORTD/CGINS-FLORTD-01121__20160930")
        declare -a OPTAA1=("None" "None")
        declare -a PCO2W1=("pco2w1" "PCO2WB/CGINS-PCO2WB-C0084__20160930")
        declare -a PHSEN1=("phsen1")
        declare -a SPKIR=("SPKIRB/CGINS-SPKIRB-00296__20160930")

        declare -a OPTAA2=("None" "None")
        declare -a PCO2W2=("pco2w2" "PCO2WB/CGINS-PCO2WB-C0053__20160930")
        declare -a PHSEN2=("phsen2")
        ;;
    "ce06issm" )
        MFN_FLAG=1
        MFN_DEPTH=29
        LAT=47.133
        LNG=-124.272
        declare -a FLORT=("FLORTD/CGINS-FLORTD-01154__20160927")
        declare -a OPTAA1=("optaa1" "OPTAAD/CGINS-OPTAAD-00136__20160927")
        declare -a PCO2W1=("pco2w1" "PCO2WB/CGINS-PCO2WB-C0085__20160927")
        declare -a PHSEN1=("phsen1")
        declare -a SPKIR=("SPKIRB/CGINS-SPKIRB-00294__20160927")

        declare -a OPTAA2=("None" "None")
        declare -a PCO2W2=("pco2w2" "PCO2WB/CGINS-PCO2WB-C0081__20160927")
        declare -a PHSEN2=("None")
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

# Buoy
$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/gps" $FNAME.gps.json
$PROCESS/process_syslog_irid.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/irid" $FNAME.syslog.json
$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/cpm1" $FNAME.superv.json
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/dcl17" $FNAME.superv.json

$PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/ctdbp" 1 $FNAME.ctdbp3.json
for mopak in $PROC/$PLATFORM/$DEPLOY/buoy/mopak/$FNAME*.mopak.json; do
    if [ -e $mopak ]; then
        SIZE=`du -k "$mopak" | cut -f1`
        if [ $SIZE -gt 0 ]; then
            $PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/mopak" $mopak
        fi
    fi
done
#--> UCSPP (acoustic modem communications with uCSPP)
$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/velpt" 1 $FNAME.velpt1.json

# NSIF
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/dcl16" $FNAME.superv.json

$PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/ctdbp" 7 $FNAME.ctdbp1.json
$PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/flort" ${FLORT[0]} $FNAME.flort.json
$PROCESS/process_nutnr.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/nutnr" $FNAME.nutnr.json
for optaa in $PROC/$PLATFORM/$DEPLOY/nsif/optaa/$FNAME*.${OPTAA1[0]}.json; do
    if [ -e $optaa ]; then
        SIZE=`du -k "$optaa" | cut -f1`
        if [ $SIZE -gt 0 ]; then
            $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/optaa" 7 ${OPTAA1[1]} $optaa
        fi
    fi
done
#$PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/pco2w" ${PCO2W1[1]} $FNAME.${PCO2W1[0]}.json
$PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/phsen" 7 $FNAME.${PHSEN1[0]}.json
$PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/spkir" ${SPKIR[0]} $FNAME.spkir.json
$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/velpt" 7 $FNAME.velpt2.json

if [ $MFN_FLAG == 1 ]; then
    # MFN
    $PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/superv/cpm3" $FNAME.superv.json
    $PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/superv/dcl35" $FNAME.superv.json
    $PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/superv/dcl37" $FNAME.superv.json

    #--> ADCPT
    $PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/ctdbp" $MFN_DEPTH $FNAME.ctdbp2.json
    #--> CAMDS
    for optaa in $PROC/$PLATFORM/$DEPLOY/mfn/optaa/$FNAME*.${OPTAA2[0]}.json; do
        if [ -e $optaa ]; then
            SIZE=`du -k "$optaa" | cut -f1`
            if [ $SIZE -gt 0 ]; then
                $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/optaa" $MFN_DEPTH ${OPTAA2[1]} $optaa
            fi
        fi
    done
    #$PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/pco2w" ${PCO2W2[1]} $FNAME.${PCO2W2[0]}.json
    $PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/phsen" $MFN_DEPTH $FNAME.${PHSEN2[0]}.json
    $PROCESS/process_presf.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/presf" $MFN_DEPTH $FNAME.presf.json
    #--> VEL3D
    #--> ZPLSC
fi
