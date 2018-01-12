#!/bin/bash
 
StartTime=""
CloseTime=""
WaitSec=10
while :
do
BATTINFO=$(acpi -b | grep Discharging)
if [ -n "$BATTINFO" ]; then	
	if [ -z "$StartTime" ]; then
		StartTime=$(date +%s)
	fi
	CloseTime=$(date +%s)
	time="$(($CloseTime - $StartTime))"
	if [ $time -gt $WaitSec ] ; then
		shutdown now
	fi
else
	StartTime=""
fi
done
