#!/usr/bin/python
from subprocess import Popen
import sys

filename = "./base_station/blue.py"
while True:
    print("\nStarting " + filename)
    p = Popen("python3 " + filename, shell = True)
    p.wait()
