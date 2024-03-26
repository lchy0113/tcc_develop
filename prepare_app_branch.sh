#!/bin/bash
#cd vendor/kdiwin/apps/

unset kd_apps
for kd_apps in $( find . -maxdepth 1 -name "wallpad-*" -print )
do
	echo $kd_apps
	git -C $kd_apps checkout release/nhn1041 ; 
	git -C $kd_apps branch --set-upstream-to=product/release/nhn1041 release/nhn1041;
	git -C $kd_apps pull ; 
	git -C $kd_apps submodule init ; 
	git -C $kd_apps submodule update ; 
	git -C $kd_apps submodule sync ; 
done
