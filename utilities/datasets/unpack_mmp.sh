#!/bin/bash
#
# Read the raw, telemetered MMP data files for the Coastal Profiler Moorings
# and create parsed datasets available in TXT files for further processing and
# review. Utilizes the mmp_unpack utility created by Jeff O'Brien of WHOI. Traps
# files that fail to process using a ulimit time-based control (should take less
# than 5 seconds to process a file).
#
# Wingard, C. 2017-02-23

# Parse the command line inputs
if [ $# -ne 2 ]; then
    echo "$0: required inputs are the platform and deployment names"
    echo "     example: $0 ce09ospm D00001"
    exit 1
fi
PLATFORM=${1,,}
DEPLOY=${2^^}

# set the MMP input and output directories
RAW="/home/ooiuser/data/raw/$PLATFORM/$DEPLOY/imm/mmp"
PROC="/home/ooiuser/data/proc/$PLATFORM/$DEPLOY/imm/mmp"
if [ ! -d $PROC ]; then
    # Make the output directory, if it doesn't exist
    /bin/mkdir -p $PROC
fi

# set the unpacker and a limit of 5 seconds for processing (takes less than a second normally)
UNPACK="/usr/bin/timeout 5 /home/ooiuser/bin/cg_util/mmp_unpack"

# setup the python parser used for creating the JSON formatted file
PYTHON="/home/ooiuser/bin/conda/bin/python"

# Process the profiler data, using the E files as the key.
for file in $RAW/E*.DAT; do
    # unpack the file, if it hasn't already been processed
    out=`/bin/basename $file`
    if [ ! -f $PROC/${out%.DAT}.TXT* ]; then
        echo "Processing $file..."

        # check to see if we already have created TIMETAGS2.TXT, don't want to overwrite
        if [ -f $PROC/TIMETAGS2.TXT ]; then
            /bin/cp $PROC/TIMETAGS2.TXT tmp
        fi

        # generate the TIMETAGS2.TXT file
        echo -e "\tGenerating TIMETAGS2"
        $UNPACK $PROC $file -t

        # check to see if we were successful
        if [ $? -eq 0 ]; then
            # Success!
            if [ -f tmp ]; then
                # If we already have an existing TIMETAGS2 file, append results
                /usr/bin/tail -1 $PROC/TIMETAGS2.TXT >> tmp
                /bin/mv tmp $PROC/TIMETAGS2.TXT
            fi
        else
            # Extract failed, create empty file indicating failure and skip to next file
            /bin/echo -e "\tCorrupted file, skipping file"
            /bin/touch $PROC/${out%.DAT}.TXT.failed
            if [ -f tmp ]; then
                # replace TIMETAGS2
                /bin/mv tmp $PROC/TIMETAGS2.TXT
            fi
            continue
        fi

        # now extract the data from the E, C, and A files
        ### Engineering and ECO Triplet data
        /bin/echo -e "\tExtracting Engineering and ECO Triplet"
        $UNPACK $PROC $file

        ### CTD and Oxygen data
        if [ -f ${file/E/C} ]; then
            /bin/echo -e "\tExtracting CTD and Oxygen"
            ctd=$PROC/${out%.DAT}.TXT
            ctd=${ctd/E/C}
            $UNPACK $PROC ${file/E/C}
            if [ $? -ne 0 ]; then
                # extract failed
                /bin/mv $ctd $ctd.failed
            fi
        fi

        ### Velocity data
        A=${file/E/A}; A=${A%.DAT}.DEC
        if [ -f $A ]; then
            /bin/echo -e "\tExtracting Velocity"
            vel=$PROC/${out%.DAT}.TXT
            vel=${vel/E/A}
            $UNPACK $PROC $A
            if [ $? -ne 0 ]; then
                # extract failed
                /bin/mv $vel $vel.failed
            fi
        fi

        ### And now we can create our JSON formatted file
        infile=$PROC/${out%.DAT}.TXT
        outfile=${infile/E/P}
        outfile=${outfile%.TXT}.json
        cd /home/ooiuser/code/cgsn-parsers
        $PYTHON -m cgsn_parsers.parsers.parse_mmp_coastal -i $infile -o $outfile
    fi
done

# clean up
/bin/rm -f tmp
