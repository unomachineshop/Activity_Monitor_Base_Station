###########################################################
# Desc: This script will continuously run the blue.py
# script to ensure that no matter what happens, the 
# script will continuously execute.
# 
# This script is used in conjunction with a cronjob which
# get executed on every single pi reboot. The combination
# of these two will not only ensure that the base station
# will run "forever", but in the even it does break, a 
# simple hard reset will bring it back to a baseline.
###########################################################
from subprocess import Popen
import sys

filename = "./base_station/blue.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell = True)
    p.wait()
