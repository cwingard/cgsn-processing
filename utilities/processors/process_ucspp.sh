#!/bin/bash -e
#
# Parse the various data files associated with a Coastal Surface Piercing Profiler
#
# Wingard, C. 2015-04-17

# Parse the command line inputs
if [ $# -ne 9 ]; then
    echo "$0: required inputs are the platform and deployment names, the latitude and "
    echo "longitude of the mooring, site depth, the data file type and the FLORT and PARAD serial numbers"
    echo ""
    echo "     example: $0 ce02shsp R00001 44.639 -124.304 25 PPB 1084 365 337"
    exit 1
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}
LAT=$3
LON=$4
DEPTH=$5
FTYPE=${6^^}
FLORT=$7
PARAD=$8
NUTNR=$9

# setup the base directories and the python parser used for creating the JSON formatted file
PROC="/home/ooiuser/data/proc/$PLATFORM/$DEPLOY"
ERDDAP="/home/ooiuser/data/erddap/$PLATFORM/$DEPLOY"
PYTHON="/home/ooiuser/bin/conda/bin/python3"

case $FTYPE in
    "ACS" )
        # OPTAA data files
        ODIR="$ERDDAP/optaa"
        COEFF="$PROC/optaa/optaa_factory_calibration.coeffs"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/optaa/ucspp_*_ACS_ACS.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_optaa -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -cf $COEFF
            fi
        done ;;

    "PPB" | "PPD" )
        # CTDPF data files
        ODIR="$ERDDAP/ctdpf"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/ctdpf/ucspp_*_"$FTYPE"_CTD.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_ctdpf -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done

        # DOSTA data files
        ODIR="$ERDDAP/dosta"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/dosta/ucspp_*_"$FTYPE"_OPT.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_dosta -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done

        # FLORT data files
        ODIR="$ERDDAP/flort"
        COEFF="$PROC/flort/flort_factory_calibration.coeffs"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/flort/ucspp_*_"$FTYPE"_TRIP.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_flort -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -sn $FLORT -cf $COEFF
            fi
        done

        # PARAD data files
        ODIR="$ERDDAP/parad"
        COEFF="$PROC/parad/parad_factory_calibration.coeffs"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/parad/ucspp_*_"$FTYPE"_PARS.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_parad -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -sn $PARAD -cf $COEFF
            fi
        done

        # SPKIR data files
        ODIR="$ERDDAP/spkir"
        COEFF="$PROC/spkir/spkir_factory_calibration.coeffs"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/spkir/ucspp_*_"$FTYPE"_OCR.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_spkir -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -cf $COEFF
            fi
        done

        # VELPT data files
        ODIR="$ERDDAP/velpt"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/velpt/ucspp_*_"$FTYPE"_ADCP.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_velpt -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done ;;

    "SNA" )
        # NUTNR data files
        ODIR="$ERDDAP/nutnr"
        COEFF="$PROC/nutnr/nutnr_inhouse_calibration.coeffs"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/nutnr/ucspp_*_SNA_SNA.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_nutnr -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH -sn $NUTNR -cf $COEFF
            fi
        done ;;

    "WC" )
        # HMR data files
        ODIR="$ERDDAP/winch"
        if [ ! -d $ODIR ]; then
            mkdir -p $ODIR
        fi
        for file in $PROC/winch/ucspp_*_WC_HMR.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_wc_hmr -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done

        # SBE data files
        for file in $PROC/winch/ucspp_*_WC_SBE.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_wc_sbe -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done

        # WM data files
        for file in $PROC/winch/ucspp_*_WC_WM.json; do
            out=`/bin/basename $file`
            if [ ! -f $ODIR/${out%.json}.nc ]; then
                echo "Processing $file..."
                cd /home/ooiuser/code/cgsn-processing
                $PYTHON -m cgsn_processing.process.proc_cspp_wc_wm -i $file -o "$ODIR/${out%.json}.nc" \
                    -p $PLATFORM -d $DEPLOY -lt $LAT -lg $LON -dp $DEPTH
            fi
        done ;;

    * )
        echo "Unknown file type, please check the name again"
        exit 0 ;;
esac
