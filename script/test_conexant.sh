#!/bin/bash

maxwait=20
progress_bar()
{
	local PROG_BAR_MAX=${1:-30}
	local PROG_BAR_DELAY=${2:-1}
	local PROG_BAR_TODO=${3:-"."}
	local PROG_BAR_DONE=${4:-"|"}
	local i

	echo -en "["
	for i in `seq 1 $PROG_BAR_MAX`
	do
		echo -en "$PROG_BAR_TODO"
	done
	echo -en "]\0015["
	for i in `seq 1 $PROG_BAR_MAX`
	do
		echo -en "$PROG_BAR_DONE"
		sleep ${PROG_BAR_DELAY}
	done
	echo
}


adb_device="F10024032709592502BE"

fail_log="cx2070x_download_firmware():.download.firmware.failed,.Error"
succ_log="cx2070x_download_firmware():.download.firmware.successfully"
test_log="cx2070x_download_firmware():"

test_cont=true
test_cnt=0
test_file=test_$(date '+%Y-%m-%d').log 

while [ $test_cont ]
do
	progress_bar $((RANDOM%$maxwait))

	echo "reboot"
	adb -s $adb_device reboot

	echo "wait-for-device"
	adb -s $adb_device wait-for-device

	if [ $(adb -s $adb_device shell dmesg | grep -c $succ_log) -ge 1 ]
	then
		echo "[`date`] [$test_cnt] success"
		echo "[`date`] [$test_cnt] success -> `adb -s $adb_device shell dmesg | grep $test_log `" >> $test_file
		test_cont=true
	elif [ $(adb -s $adb_device shell dmesg | grep -c $fail_log) -ge 1 ]
	then
		echo "[`date`] [$test_cnt] fail" >> $test_file
		echo "[`date`] [$test_cnt] fail -> `adb -s $adb_device shell dmesg | grep $test_log `" >> $test_file
		test_cont=false
	fi
	test_cnt=$((test_cnt+1))
done


echo "[`date`] test finish test_cnt($test_cnt)"
