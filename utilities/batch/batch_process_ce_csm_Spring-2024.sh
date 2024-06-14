#!/bin/bash -e
#
# Process the various data files for a Coastal Endurance Coastal Surface
# Mooring from the Spring 2024 Deployment (Endurance 20).
#
# Wingard, C. 2024-05-02 -- Initial version

# Parse the command line inputs
if [ $# -ne 2 ]; then
    echo "$0: required inputs are the platform and deployment name."
    echo "     example: $0 ce02shsm D00018"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}

# Set some instrument names and processing flags based on the platform name
case "$PLATFORM" in
    "ce02shsm" )
        MFN_FLAG=0
        LAT="44.639"
        LON="-124.304"
        CTD1="ctdbp"
        FLR="1291"
        PH1="P0125"
        ;;
    "ce04ossm" )
        MFN_FLAG=0
        LAT=44.381
        LON=-124.956
        CTD1="ctdbp"
        FLR="1153"
        PH1="P0122"
        ;;
    "ce07shsm"  )
        MFN_FLAG=1
        MFN_DEPTH=87
        LAT=46.986
        LON=-124.566
        CTD1="ctdbp1"
        FLR="1302"
        PCO2="C0081"
        PH1="P0166"
        PH2="P0083"
        ZPLSC=5.016
        ;;
    "ce09ossm" )
        MFN_FLAG=1
        MFN_DEPTH=542
        LAT=46.851
        LON=-124.972
        CTD1="ctdbp1"
        FLR="996"
        PCO2="C0053"
        PH1="P0086"
        PH2="P0118"
        ZPLSC=5.096
        ;;
    * )
        echo "Unknown platform, please check the name again"
        exit 0 ;;
esac

# set the directory for the parsed data and the processing scripts
PARSED="/home/ooiuser/data/parsed/$PLATFORM/$DEPLOY"
PROCESS="/home/ooiuser/code/cgsn-processing/utilities/processors"

# set the absolute path to the polling script
POLLING="/home/ooiuser/code/cgsn-parsers/utilities/harvesters/polling.sh"

# load the ooi python environment
source /home/ooiuser/miniconda/bin/activate ooi-old

#### Buoy Instruments ####
assembly="buoy"  # surface buoy with CPM1 (and auxiliary sensors/instruments)
depth=0.0
# control systems
$POLLING "$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/cpm1" "$PARSED/$assembly/superv/cpm1/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl11" "$PARSED/$assembly/superv/dcl11/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl12" "$PARSED/$assembly/superv/dcl12/*.superv.json"
$POLLING "$PROCESS/process_gps.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly gps" "$PARSED/$assembly/gps/*.gps.json"
$POLLING "$PROCESS/process_syslog_irid.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly irid" "$PARSED/$assembly/irid/*.syslog.json"
$POLLING "$PROCESS/process_pwrsys.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly psc" "$PARSED/$assembly/psc/*.pwrsys.json"

# instruments
$POLLING "$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly hyd1" "$PARSED/$assembly/hyd1/*.hyd1.json"
$POLLING "$PROCESS/process_hydgn.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly hyd2" "$PARSED/$assembly/hyd2/*.hyd2.json"
$POLLING "$PROCESS/process_mopak.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly mopak" "$PARSED/$assembly/mopak/*.mopak.json"
$POLLING "$PROCESS/process_metbk.sh $PLATFORM $DEPLOY $LAT $LON -4.0 $assembly metbk" "$PARSED/$assembly/metbk/*.metbk.json"
$POLLING "$PROCESS/process_swnd.sh $PLATFORM $DEPLOY $LAT $LON -4.0 $assembly metwnd" "$PARSED/$assembly/metwnd/*.metwnd.json"
$POLLING "$PROCESS/process_pco2a.sh -c metbk $PLATFORM $DEPLOY $LAT $LON $depth $assembly pco2a" "$PARSED/$assembly/pco2a/*.pco2a.json"
$POLLING "$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON 1.5 $assembly velpt" "$PARSED/$assembly/velpt/*.velpt*.json"
$POLLING "$PROCESS/process_wavss.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly wavss" "$PARSED/$assembly/wavss/*.wavss.json"
if [ $PLATFORM = "ce02shsm" ]; then
    $POLLING "$PROCESS/process_fdchp.sh $PLATFORM $DEPLOY $LAT $LON -4.0 $assembly fdchp" "$PARSED/$assembly/fdchp/*.fdchp.json"
fi

#### NSIF Instruments ####
assembly="nsif"  # midwater platform with CPM2 (no auxiliary sensors/instruments)
depth=7.0
# control systems
$POLLING "$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/cpm2" "$PARSED/$assembly/superv/cpm2/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl26" "$PARSED/$assembly/superv/dcl26/*.superv.json"
$POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl27" "$PARSED/$assembly/superv/dcl27/*.superv.json"

# instruments
$POLLING "$PROCESS/process_ctdbp.sh -f solo $PLATFORM $DEPLOY $LAT $LON $depth $assembly ctdbp" "$PARSED/$assembly/ctdbp/*.ctdbp*.json"
$POLLING "$PROCESS/process_adcp.sh -f pd0 -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly adcp" "$PARSED/$assembly/adcp/*.adcp*.json"
$POLLING "$PROCESS/process_dosta.sh -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly dosta" "$PARSED/$assembly/dosta/*.dosta.json"
$POLLING "$PROCESS/process_flort.sh -c $CTD1 -s $FLR $PLATFORM $DEPLOY $LAT $LON $depth $assembly flort" "$PARSED/$assembly/flort/*.flort.json"
$POLLING "$PROCESS/process_suna.sh -c $CTD1 $PLATFORM $DEPLOY $LAT $LON $depth $assembly nutnr" "$PARSED/$assembly/nutnr/*.nutnr.json"
$POLLING "$PROCESS/process_optaa.sh -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly optaa" "$PARSED/$assembly/optaa/*.optaa*.json"
$POLLING "$PROCESS/process_phsen.sh -c ctdbp -s $PH1 $PLATFORM $DEPLOY $LAT $LON $depth $assembly phsen" "$PARSED/$assembly/phsen/*.phsen*.json"
$POLLING "$PROCESS/process_spkir.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly spkir" "$PARSED/$assembly/spkir/*.spkir.json"
$POLLING "$PROCESS/process_velpt.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly velpt" "$PARSED/$assembly/velpt/*.velpt*.json"

# test instruments
if [ $PLATFORM = "ce02shsm" ]; then
    $POLLING "$PROCESS/process_co2pro.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly pco2test" "$PARSED/$assembly/pco2test/*.pco2test.json"
    $POLLING "$PROCESS/process_cphox.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly phtest" "$PARSED/$assembly/phtest/*.phtest.json"
fi

#### MFN Instruments ####
if [ $MFN_FLAG == 1 ]; then
    assembly="mfn"  # seafloor platform with CPM3 (and the MPEA)
    depth=$MFN_DEPTH
    # control systems
    $POLLING "$PROCESS/process_superv_cpm.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/cpm3" "$PARSED/$assembly/superv/cpm3/*.superv.json"
    $POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl36" "$PARSED/$assembly/superv/dcl36/*.superv.json"
    $POLLING "$PROCESS/process_superv_dcl.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly superv/dcl37" "$PARSED/$assembly/superv/dcl37/*.superv.json"
    $POLLING "$PROCESS/process_mpea.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly mpea" "$PARSED/$assembly/mpea/*.pwrsys.json"

    # instruments
    $POLLING "$PROCESS/process_ctdbp.sh -f dosta $PLATFORM $DEPLOY $LAT $LON $depth $assembly ctdbp" "$PARSED/$assembly/ctdbp/*.ctdbp2.json"
    $POLLING "$PROCESS/process_adcp.sh -f pd0 -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly adcp" "$PARSED/$assembly/adcp/*.adcp*.json"
    $POLLING "$PROCESS/process_optaa.sh -c ctdbp $PLATFORM $DEPLOY $LAT $LON $depth $assembly optaa" "$PARSED/$assembly/optaa/*.optaa*.json"
    $POLLING "$PROCESS/process_pco2w.sh -s $PCO2 $PLATFORM $DEPLOY $LAT $LON $depth $assembly pco2w" "$PARSED/$assembly/pco2w/*.pco2w.json"
    $POLLING "$PROCESS/process_phsen.sh -c ctdbp -s $PH2 $PLATFORM $DEPLOY $LAT $LON $depth $assembly phsen" "$PARSED/$assembly/phsen/*.phsen*.json"
    $POLLING "$PROCESS/process_presf.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly presf" "$PARSED/$assembly/presf/*.presf.json"
    #$POLLING "$PROCESS/process_vel3d.sh $PLATFORM $DEPLOY $LAT $LON $depth $assembly vel3d" "$PARSED/$assembly/vel3d/*.vel3d.json"
    $POLLING "$PROCESS/process_zplsc.sh -f $ZPLSC $PLATFORM $DEPLOY $LAT $LON $depth $assembly zplsc" "$PARSED/$assembly/zplsc/*.zplsc.json"
fi
