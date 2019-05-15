nmea_navsat_driver
===============

ROS driver to parse NMEA strings and publish standard ROS NavSat message types. Does not require the GPSD daemon to be running.

API
---

This package has no released Code API.

The ROS API documentation and other information can be found at http://ros.org/wiki/nmea_navsat_driver


Post processing
---

To post process data, please follow these steps:

- Download the logs from the reference and the mobile station
- Download Emlid RTKLIB from https://docs.emlid.com/reachm-plus/common/tutorials/gps-post-processing/
- Follow the rest of the steps in https://docs.emlid.com/reachm-plus/common/tutorials/gps-post-processing/ until you are able to plot the trajectory with RTKPLOT
