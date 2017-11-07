#!/bin/bash

# Set deployment numbers for the moorings
CE01="D00008"
CE02="D00006"
CE04="D00005"
CE06="D00007"
CE07="D00006"
CE09="D00006"
CE09P="D00008"
CRUISE="Fall-2017"

# process the daily log files
cd /home/ooiuser/code/cgsn-processing
START=$(( (`date -d --now +%s` - `date -d '2017/10/03' +%s`) / (24*3600) ))
END=0
for (( day=$START; day>=$END; day-- )); do
    echo "Processing CE01ISSM $CE01 day $day"; ./utilities/processors/process_CE_ISM_$CRUISE.sh ce01issm $CE01 $day
    echo "Processing CE02SHSM $CE02 day $day"; ./utilities/processors/process_CE_CSM_$CRUISE.sh ce02shsm $CE02 $day
    echo "Processing CE04OSSM $CE04 day $day"; ./utilities/processors/process_CE_CSM_$CRUISE.sh ce04ossm $CE04 $day
    echo "Processing CE06ISSM $CE06 day $day"; ./utilities/processors/process_CE_ISM_$CRUISE.sh ce06issm $CE06 $day
    echo "Processing CE07SHSM $CE07 day $day"; ./utilities/processors/process_CE_CSM_$CRUISE.sh ce07shsm $CE07 $day
    echo "Processing CE09OSSM $CE09 day $day"; ./utilities/processors/process_CE_CSM_$CRUISE.sh ce09ossm $CE09 $day
    echo "Processing CE09OSPM $CE09P day $day"; ./utilities/processors/process_CE_PM_$CRUISE.sh ce09ospm $CE09P $day
done
