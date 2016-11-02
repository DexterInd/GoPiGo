#! /bin/bash

id=$(ps aux | grep "python GoPiGoScratch.py" | grep -v grep | awk '{print $2}')
kill -15 $id 2> /dev/null
python /home/pi/Desktop/GoPiGo/Software/Scratch/GoPiGoScratch.py
