#!/bin/bash

if [ \
        -e /dev/ttyUSB3 -o \
            "$(cat /sys/class/net/ppp0/operstate 2> /dev/null)" = up ]
then
        exit 0
fi

/bin/ping -c1 8.8.8.8 | grep "bytes from" &> /dev/null 2> /dev/null

if [ "$?" -ne 0 ]; then
        exit 0
fi

np=/usr/lib/nagios/plugins
lp=/usr/local/lib/nagios/plugins

submit_check() {
#    echo ${1}
    out="$(${2})"
    ssh root@amnesia.muzybot.de "icinga_submit_check jupiter '${1}' ${?} '${out}'"
    sleep 3
}

INTERVAL="${1}"

if [ "${INTERVAL}" == "veryoft" ]
then
     submit_check 'HDD_TEMP' "/usr/bin/sudo ${lp}/check_hddtemp /dev/sda 50 55"
     submit_check 'CPU_TEMP' "/usr/bin/sudo ${lp}/check_cputemp 70 75"
     submit_check 'LOAD' "${np}/check_load --warning=5,4,3 --critical=8,5,5"
     submit_check 'VPN' "${np}/check_ping -H 10.0.0.1 -w 5000,100% -c 5000,100% -p 1"
elif [ "${INTERVAL}" == "oft" ]
then
    submit_check 'SMART' "/usr/bin/sudo ${np}/check_ide_smart -n -d /dev/sda"
    submit_check 'DISK_HOME' "${np}/check_disk -w 10% -c 5% -p /"
    submit_check 'DISK_ROOT' "${np}/check_disk -w 10% -c 5% -p /home"
elif [ "${INTERVAL}" == "rare" ]
then
    submit_check 'APT' "/usr/bin/sudo ${np}/check_apt -u -d -t 100"
fi
