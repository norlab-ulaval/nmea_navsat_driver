#!/bin/bash

while :
do
ROSPROG=$(ps cax | grep ros)
PYPROG=$(ps cax | grep python)
if [ -z "$ROSPROG" ] || [ -z "$PYPROG" ]; then
    killall python
    killall roscore
    roscore &
    rosrun nmea_navsat_driver nmea_tcp_driver &
    sleep 1
fi
done