###########################################################
# Desc: This script will continuously run the blue.py
# script to ensure that no matter what happens, the 
# script will continuously execute.
# 
# This script is used in conjunction with a cronjob which
# get executed on every single pi reboot. The combination
# of these two will not only ensure that the base station
# will run "forever", but in the event it does break, a 
# simple hard reset will bring it back to a baseline.
###########################################################
from subprocess import Popen
import sys
import time

filename = "./base_station/blue.py"
while True:
    print("\nStarting " + filename)
    cmd = ['python3', filename]
    p = Popen(cmd)
    p.wait()
    time.sleep(60) # Brief pause
