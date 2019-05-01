import time
import sys
import uuid
import argparse
import os
import ibmiotf.device
from pathlib import Path


class DeviceClient():
    
    ##########################################################
    # Name: init
    # Desc: Declaration of some class wide variables. 
    ##########################################################
    def __init__(self):
        self.options = ""
        self.client = ""
    

    ##########################################################
    # Name: command_processor
    # Desc: Handles an incoming message from the cloud.
    ##########################################################
    # Command processing function for specified device
    def command_processor(self, cmd):
        print("Command received: %s" % cmd.data)

    
    ##########################################################
    # Name: connect_to_cloud
    # Desc: Loads up the config file 'device.cfg', and with
    # those options, connects to specified cloud instance.
    ##########################################################
    def connect_to_cloud(self):
        try:
            # Retrieve config file parameters from config file located in same working directory
            #options = ibmiotf.device.ParseConfigFile(os.path.join(Path().absolute(), "device.cfg"))                     # Windows
            self.options = ibmiotf.device.ParseConfigFile("/home/pi/Activity_Monitor_Base_Station/iot_cloud/device.cfg") # Linux
            # Apply config file parameters to client device
            self.client = ibmiotf.device.Client(self.options)
            # Define the callback function for client device
            self.client.commandCallback = self.command_processor
            # Connect the device to IBM Watson
            self.client.connect()

        except ibmiotf.ConnectionException as e:
            print("Caught exception connecting device: %s" % str(e))
            sys.exit()

    
    ##########################################################
    # Name: send_to_cloud
    # Desc: Sends the ordered dictionary of information to
    # the cloud, as a JSON structure. 
    ##########################################################
    def send_to_cloud(self, data):

        success = self.client.publishEvent("event", "json", data, qos=0)

        if not success:
            print("Publish event failed!")
            sys.exit() #Watch out for this!!!
    

    ##########################################################
    # Name: disconnect_from_cloud
    # Desc: Disconnect from the IBM IoT cloud.
    ##########################################################
    def disconnect_from_cloud(self):
        self.client.disconnect()

