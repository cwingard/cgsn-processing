#!/bin/bash -e
#
# Parse the various data files for a Coastal Surface Mooring.
#
# Wingard, C. 2017-02-15

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

PROC="/webdata/cgsn/data/proc"
PROCESS="/home/cgsnmo/dev/cgsn-processing/utilities/processors"

# Set some instrument names and processing flags based on the platform name
case "$PLATFORM" in
    "ce02shsm" )
        MFN_FLAG=0
        LAT="44.63893"
        LNG="-124.30379"
        declare -a CTDBP1=("ctdbp")
        declare -a FLORT=("FLORTD/CGINS_FLORTD_01153__20160926")
        declare -a OPTAA1=("optaa" "OPTAAD/CGINS-OPTAAD-00168__20160926")
        declare -a PHSEN1=("phsen")
        declare -s SPKIR=("SPKIRB/CGINS_SPKIRB_00242__20160926")
        ;;
    "ce04ossm" )
        MFN_FLAG=0
        LAT="44.38357"
        LNG="-124.95499"
        declare -a CTDBP1=("ctdbp")
        declare -a FLORT=("FLORTD/CGINS_FLORTD_01303__20161001")
        declare -a OPTAA1=("optaa" "OPTAAD/CGINS-OPTAAD-00258__20161001")
        declare -a PHSEN1=("phsen")
        declare -s SPKIR=("SPKIRB/CGINS_SPKIRB_00249__20161001")
        ;;
    "ce07shsm"  )
        MFN_FLAG=1
        MFN_DEPTH=87
        LAT="46.98589"
        LNG="-124.56490"
        declare -a CTDBP1=("ctdbp1")
        declare -a FLORT=("FLORTD/CGINS_FLORTD_00996__20160921")
        declare -a OPTAA1=("optaa1" "OPTAAD/CGINS-OPTAAD-00208__20160921")
        declare -a PHSEN1=("phsen1")
        declare -s SPKIR=("SPKIRB/CGINS_SPKIRB_00254__20160921")

        declare -a OPTAA2=("None" "None")
        declare -a PCO2W=("pco2w" "PCO2WB/CGINS-PCO2WB-C0082__20160921")
        declare -a PHSEN2=("phsen2")
        ;;
    "ce09ossm" )
        MFN_FLAG=1
        MFN_DEPTH=542
        LAT="46.85025"
        LNG="-124.97030"
        declare -a CTDBP1=("ctdbp1")
        declare -a FLORT=("FLORTD/CGINS_FLORTD_01291__20160920")
        declare -a OPTAA1=("optaa1" "OPTAAD/CGINS-OPTAAD-00124__20160920")
        declare -a PHSEN1=("phsen1")
        declare -s SPKIR=("SPKIRB/CGINS_SPKIRB_00243__20160920")

        declare -a OPTAA2=("optaa2" "OPTAAC/CGINS-OPTAAC-00266__20160920")
        declare -a PCO2W=("pco2w" "PCO2WB/CGINS-PCO2WB-C0062__20160920")
        declare -a PHSEN2=("phsen2")
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

# Buoy
$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/gps" $FNAME.gps.json
$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/hydgn" $FNAME.hyd1.json
$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/hydgn" $FNAME.hyd2.json
for mopak in $PROC/$PLATFORM/$DEPLOY/buoy/mopak/$FNAME*.mopak.json; do
    if [ -e $mopak ]; then
        SIZE=`du -k "$mopak" | cut -f1`
        if [ $SIZE > 0 ]; then
            $PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/mopak" $mopak
        fi
    fi
done
$PROCESS/process_pwrsys.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/pwrsys" $FNAME.pwrsys.json
$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/cpm1" $FNAME.superv.json
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/dcl11" $FNAME.superv.json
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/superv/dcl12" $FNAME.superv.json

if [ $PLATFORM = "ce02shsm" ]; then
    $PROCESS/process_fdchp.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/fdchp" $FNAME.fdchp.json
fi
$PROCESS/process_metbk.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/metbk" $FNAME.metbk.json
$PROCESS/process_pco2a.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/pco2a" $FNAME.pco2a.json
$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/velpt" 1 $FNAME.velpt1.json
$PROCESS/process_wavss.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/wavss" $FNAME.wavss.json

# NSIF
$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/superv/cpm2" $FNAME.superv.json
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/superv/dcl26" $FNAME.superv.json
$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/superv/dcl27" $FNAME.superv.json

#--> ADCPT
$PROCESS/process_ctdbp.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/ctdbp" 7 $FNAME.${CTDBP1[0]}.json
$PROCESS/process_dosta.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/dosta" 7 $FNAME.${DOSTA1[0]}.json
$PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/flort" 7 ${FLORT[0]} $FNAME.flort.json
$PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/nutnr" 7 $FNAME.nutnr.json
for optaa in $PROC/$PLATFORM/$DEPLOY/nsif/optaa/$FNAME*.${OPTAA1[0]}.json; do
    if [ -e $optaa ]; then
        SIZE=`du -k "$optaa" | cut -f1`
        if [ $SIZE > 0 ]; then
            $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/optaa" 7 ${OPTAA1[1]} $optaa
        fi
    fi
done
$PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/phsen" 7 $FNAME.${PHSEN1[0]}.json
$PROCESS/process_flort.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/spkir" 7 ${SPKIR[0]} $FNAME.spkir.json
#--> UCSPP (acoustic modem communications with uCSPP)
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
            if [ $SIZE > 0 ]; then
                $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/optaa" $MFN_DEPTH ${OPTAA2[1]} $optaa
            fi
        fi
    done
    #$PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/pco2w" $MFN_DEPTH ${PCO2W[1]} $FNAME.${PCO2W[0]}.json
    $PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/phsen" $MFN_DEPTH $FNAME.${PHSEN2[0]}.json
    $PROCESS/process_presf.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/presf" $MFN_DEPTH $FNAME.presf.json
    #--> VEL3D
    #--> ZPLSC
fi
