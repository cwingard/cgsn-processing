#!/bin/bash

# Set deployment numbers for the moorings
CE01="D00008"
CE02="D00006"
CE04="D00005"
CE06="D00007"
CE07="D00006"
CE09="D00006"
CE09P="D00008"

# process the daily log files
cd /home/ooiuser/code/cgsn-parsers
START=$(( (`date -d --now +%s` - `date -d '2017/10/03' +%s`) / (24*3600) ))
END=0
for (( day=$START; day>=$END; day-- )); do
    echo "Harvesting CE01ISSM $CE01 day $day"; ./utilities/harvesters/master_harvester_ism.sh ce01issm $CE01 $day
    echo "Harvesting CE02SHSM $CE02 day $day"; ./utilities/harvesters/master_harvester_ce_csm.sh ce02shsm $CE02 $day
    echo "Harvesting CE04OSSM $CE04 day $day"; ./utilities/harvesters/master_harvester_ce_csm.sh ce04ossm $CE04 $day
    echo "Harvesting CE06ISSM $CE06 day $day"; ./utilities/harvesters/master_harvester_ism.sh ce06issm $CE06 $day
    echo "Harvesting CE07SHSM $CE07 day $day"; ./utilities/harvesters/master_harvester_ce_csm.sh ce07shsm $CE07 $day
    echo "Harvesting CE09OSSM $CE09 day $day"; ./utilities/harvesters/master_harvester_ce_csm.sh ce09ossm $CE09 $day
    echo "Harvesting CE09OSPM $CE09P day $day"; ./utilities/harvesters/master_harvester_pm.sh ce09ospm $CE09P $day
done
