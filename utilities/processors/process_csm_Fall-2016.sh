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
        declare -a OPTAA1=("optaa" "OPTAAD/CGINS-OPTAAD-00168__20160926")
        declare -a PHSEN1=("phsen" "7")
        ;;
    "ce04ossm" )
        MFN_FLAG=0
        LAT="44.38357"
        LNG="-124.95499"
        declare -a OPTAA1=("optaa" "OPTAAD/CGINS-OPTAAD-00258__20161001")
        declare -a PHSEN1=("phsen" "7")
        ;;
    "ce07shsm"  )
        MFN_FLAG=1
        LAT="46.98589"
        LNG="-124.56490"
        declare -a OPTAA1=("optaa1" "OPTAAD/CGINS-OPTAAD-00208__20160921")
        declare -a PHSEN1=("phsen1" "7")
        
        declare -a OPTAA2=("None" "None")
        declare -a PCO2W=("pco2w" "PCO2WB/CGINS-PCO2WB-C0082__20160921")
        declare -a PHSEN2=("phsen2" "87")
        ;;
    "ce09ossm" )
        MFN_FLAG=1
        LAT="46.85025"
        LNG="-124.97030"
        declare -a OPTAA1=("optaa1" "OPTAAD/CGINS-OPTAAD-00124__20160920")
        declare -a PHSEN1=("phsen1" "7")

        declare -a OPTAA2=("optaa2" "OPTAAC/CGINS-OPTAAC-00266__20160920")
        declare -a PCO2W=("pco2w" "PCO2WB/CGINS-PCO2WB-C0062__20160920")
        declare -a PHSEN2=("phsen2" "542")
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

# Buoy
$PROCESS/process_pwrsys.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/pwrsys" $FNAME.pwrsys.json

$PROCESS/process_metbk.sh $PLATFORM $DEPLOY $LAT $LNG "buoy/metbk" $FNAME.metbk.json
#--> MOPAK
#--> PCO2A
#--> VELPT
#--> WAVSS

# NSIF
#--> ADCPT
#--> CTDBP
#--> DOSTA
#--> FLORT
#--> NUTNR
#for optaa in $PROC/$PLATFORM/$DEPLOY/nsif/optaa/$FNAME*.${OPTAA1[0]}.json; do
#    if [ -e $optaa ]; then
#        SIZE=`du -k "$optaa" | cut -f1`
#        if [ $SIZE > 0 ]; then
#            $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/optaa" ${OPTAA1[1]} $optaa
#        fi
#    fi
#done
#$PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "nsif/phsen" ${PHSEN1[1]} $FNAME.${PHSEN1[0]}.json
#--> SPKIR
#--> UCSPP (acoustic modem communications with uCSPP)
#--> VELPT

#if [ $MFN_FLAG == 1 ]; then
    # MFN
    #--> ADCPT
    #--> CTDBP + DOSTA
    #--> CAMDS
#    for optaa in $PROC/$PLATFORM/$DEPLOY/mfn/optaa/$FNAME*.${OPTAA2[0]}.json; do
#        if [ -e $optaa ]; then
#            SIZE=`du -k "$optaa" | cut -f1`
#            if [ $SIZE > 0 ]; then
#                $PROCESS/process_optaa.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/optaa" ${OPTAA2[1]} $optaa
#            fi
#        fi
#    done
#    $PROCESS/process_pco2w.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/pco2w" ${PCO2W[1]} $FNAME.${PCO2W[0]}.json
#    $PROCESS/process_phsen.sh $PLATFORM $DEPLOY $LAT $LNG "mfn/phsen" ${PHSEN1[1]} $FNAME.${PHSEN2[0]}.json
    #--> PRESF
    #--> VEL3D
    #--> ZPLSC
#fi
