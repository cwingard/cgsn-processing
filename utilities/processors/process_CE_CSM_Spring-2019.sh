#!/bin/bash -e
#
# Parse the various data files from the OOI Endurance Array Coastal Surface
# Moorings (CSM) collected during the course of the Spring 2019 deployment.
# This script is intended to serve as a guide for how a user might go about
# processing the data. There are other ways of processing the data that are
# more efficient.
#
# Wingard, C. 2021-08-20

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
source activate ooi

# Set some instrument names and processing flags based on the platform name
case "$PLATFORM" in
    "ce02shsm" )
        MFN_FLAG=0
        LAT="44.639"
        LON="-124.304"
        declare -a ADCP1=("adcpt")
        declare -a CTDBP1=("ctdbp")
        declare -a FLORT=("1290")
        declare -a OPTAA1=("optaa")
        declare -a PHSEN1=("phsen")
        ;;
    "ce04ossm" )
        MFN_FLAG=0
        LAT="44.381"
        LON="-124.956"
        declare -a ADCP1=("adcpt")
        declare -a CTDBP1=("ctdbp")
        declare -a FLORT=("1488")
        declare -a OPTAA1=("optaa")
        declare -a PHSEN1=("phsen")
        ;;
    "ce07shsm"  )
        MFN_FLAG=1
        MFN_DEPTH=87
        LAT="46.986"
        LON="-124.566"
        declare -a ADCP1=("adcpt1")
        declare -a CTDBP1=("ctdbp1")
        declare -a FLORT=("1487")
        declare -a OPTAA1=("optaa1")
        declare -a PHSEN1=("phsen1")

        declare -a ADCP2=("adcpt2")
        declare -a OPTAA2=("optaa2")
        declare -a PCO2W=("C0052")
        declare -a PHSEN2=("phsen2")
        declare -a ZPLSC=(5.016)
        ;;
    "ce09ossm" )
        MFN_FLAG=1
        MFN_DEPTH=542
        LAT="46.851"
        LON="-124.972"
        declare -a ADCP1=("adcpt")
        declare -a CTDBP1=("ctdbp1")
        declare -a FLORT=("1123")
        declare -a OPTAA1=("optaa1")
        declare -a PHSEN1=("phsen1")

        declare -a ADCP2=("adcps")
        declare -a OPTAA2=("optaa2")
        declare -a PCO2W=("C0147")
        declare -a PHSEN2=("phsen2")
        declare -a ZPLSC=(5.096)
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

# Buoy
#$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LON "buoy/gps" $FNAME.gps.json
#$PROCESS/process_syslog_irid.sh $PLATFORM $DEPLOY $LAT $LON "buoy/irid" $FNAME.syslog.json
#$PROCESS/process_syslog_fb250.sh $PLATFORM $DEPLOY $LAT $LON "buoy/fb250" $FNAME.syslog.json
#$PROCESS/process_syslog_rda.sh $PLATFORM $DEPLOY $LAT $LON "buoy/rda" $FNAME.syslog.json
#$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LON "buoy/hydgn" $FNAME.hyd1.json
#$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LON "buoy/hydgn" $FNAME.hyd2.json
#for mopak in $PROC/$PLATFORM/$DEPLOY/buoy/mopak/$FNAME*.mopak.json; do
#    if [ -e $mopak ]; then
#        SIZE=`du -k "$mopak" | cut -f1`
#        if [ $SIZE -gt 0 ]; then
#            $PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LON "buoy/mopak" $mopak
#        fi
#    fi
#done
#$PROCESS/process_pwrsys.sh $PLATFORM $DEPLOY $LAT $LON "buoy/pwrsys" $FNAME.pwrsys.json
#$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON "buoy/superv/cpm1" 0 $FNAME.superv.json
#$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "buoy/superv/dcl11" 0 $FNAME.superv.json
#$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "buoy/superv/dcl12" 0 $FNAME.superv.json

#if [ $PLATFORM = "ce02shsm" ]; then
#    $PROCESS/process_fdchp.sh $PLATFORM $DEPLOY $LAT $LON "buoy/fdchp" $FNAME.fdchp.json
#fi
#$PROCESS/process_metbk.sh $PLATFORM $DEPLOY $LAT $LON "buoy/metbk" $FNAME.metbk.json
#$PROCESS/process_pco2a.sh $PLATFORM $DEPLOY $LAT $LON "buoy/pco2a" $FNAME.pco2a.json
#$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON "buoy/velpt" 1 $FNAME.velpt1.json
#$PROCESS/process_wavss.sh $PLATFORM $DEPLOY $LAT $LON "buoy/wavss" $FNAME.wavss.json

# NSIF
#$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON "nsif/superv/cpm2" 7 $FNAME.superv.json
#$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "nsif/superv/dcl26" 7 $FNAME.superv.json
#$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "nsif/superv/dcl27" 7 $FNAME.superv.json
#
#$PROCESS/process_adcp.sh $PLATFORM $DEPLOY $LAT $LON "nsif/adcp" "ctdbp" 7 $FNAME.${ADCP1[0]}.json
#$PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LON "nsif/ctdbp" 7 0 "solo" $FNAME.${CTDBP1[0]}.json
$PROCESS/process_dosta.sh $PLATFORM $DEPLOY $LAT $LON "nsif/dosta" 7 $FNAME.dosta.json
$PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LON "nsif/flort" "ctdbp" 7 ${FLORT[0]} $FNAME.flort.json
#$PROCESS/process_suna.sh $PLATFORM $DEPLOY $LAT $LON "nsif/nutnr" ${CTDBP1[0]} 7 $FNAME.nutnr.json
for optaa in $PROC/$PLATFORM/$DEPLOY/nsif/optaa/$FNAME*.${OPTAA1[0]}.json; do
    if [ -e $optaa ]; then
        SIZE=`du -k "$optaa" | cut -f1`
        if [ $SIZE -gt 0 ]; then
            $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LON "nsif/optaa" 7 $optaa
        fi
    fi
done
#$PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LON "nsif/phsen" 7 $FNAME.${PHSEN1[0]}.json
#$PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LON "nsif/spkir" 7 $FNAME.spkir.json
#$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON "nsif/velpt" 7 $FNAME.velpt2.json

if [ $MFN_FLAG == 1 ]; then
    # MFN
#    $PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON "mfn/superv/cpm3" $MFN_DEPTH $FNAME.superv.json
#    $PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "mfn/superv/dcl36" $MFN_DEPTH $FNAME.superv.json
#    $PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON "mfn/superv/dcl37" $MFN_DEPTH $FNAME.superv.json
#    $PROCESS/process_mpea.sh $PLATFORM $DEPLOY $LAT $LON "mfn/pwrsys" $MFN_DEPTH $FNAME.pwrsys.json

#    $PROCESS/process_adcp.sh $PLATFORM $DEPLOY $LAT $LON "mfn/adcp" "ctdbp" $MFN_DEPTH $FNAME.${ADCP2[0]}.json
#    $PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LON "mfn/ctdbp" $MFN_DEPTH 0 "dosta" $FNAME.ctdbp2.json
    for optaa in $PROC/$PLATFORM/$DEPLOY/mfn/optaa/$FNAME*.${OPTAA2[0]}.json; do
        if [ -e $optaa ]; then
            SIZE=`du -k "$optaa" | cut -f1`
            if [ $SIZE -gt 0 ]; then
                $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LON "mfn/optaa" $MFN_DEPTH $optaa
            fi
        fi
    done
#    $PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LON "mfn/pco2w" $MFN_DEPTH ${PCO2W[0]} $FNAME.pco2w.json
#    $PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LON "mfn/phsen" $MFN_DEPTH $FNAME.${PHSEN2[0]}.json
#    $PROCESS/process_presf.sh $PLATFORM $DEPLOY $LAT $LON "mfn/presf" $MFN_DEPTH $FNAME.presf.json
#    $PROCESS/process_vel3d.sh $PLATFORM $DEPLOY $LAT $LON "mfn/vel3d" $MFN_DEPTH $FNAME.vel3d.json
#    $PROCESS/process_zplsc.sh $PLATFORM $DEPLOY $LAT $LON "mfn/zplsc" $MFN_DEPTH ${ZPLSC[0]} $FNAME.zplsc.json
fi
