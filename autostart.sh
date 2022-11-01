#!/usr/bin/bash

DATE=`/bin/date +"%Y-%m-%d_%H.%M"`
cd /home/raspberry/Desktop/ip/
stdbuf -oL /usr/bin/python3 ip.py > logs/ip_${DATE}.log 2>&1

