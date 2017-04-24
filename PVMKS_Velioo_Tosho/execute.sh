#!/bin/sh
raspistill -o test.png -t 100 -w 1600 -h 1200
sleep 1
export GOOGLE_APPLICATION_CREDENTIALS=google_servicekey.json
source ~/.bashrc
python camera-vision-label-test.py
