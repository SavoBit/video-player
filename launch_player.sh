#!/bin/bash

killall MP4Client
sleep 1
python3 punch_ran.py
sleep 1
#MP4Client session.sdp
python2.7 player.py --start
