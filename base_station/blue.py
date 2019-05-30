import binascii
import struct
import time
from struct import *
from datetime import datetime
from bluepy.btle import DefaultDelegate, Peripheral, Scanner
from collections import OrderedDict
from collections import deque

# Asynchronous delegates
from notification_delegate import NotificationDelegate
from scan_delegate import ScanDelegate

# Box
import sys
sys.path.append("/home/pi/Activity_Monitor_Base_Station/box")
from box import Box 

# IBM Watson IoT (NOT IN USE)
#import sys
#sys.path.append("/home/pi/Activity_Monitor_Base_Station/iot_cloud")
#from device_client import DeviceClient



############################################################
# Name: within_range
# Desc: Attempts to find whether the specified device is 
# within a usable range. A scan is performed to search for
# the specified device, as well as an RSSI check for an
# optimal connection.
############################################################
def within_range(mac):
    SCAN_DURATION = 10.0
    MIN_RSSI = -101

    scanner = Scanner().withDelegate(ScanDelegate())
    devices = scanner.scan(SCAN_DURATION)

    for dev in devices:
        if dev.addr == mac and dev.rssi > MIN_RSSI:
            print("Device was found!")
            return True

    time.sleep(1)
    print("Device wasn't found...")
    return False

#######################################################
# Name: connection_checks
# Desc: Used in conjunction with within_range(). Will
# run a series of three tests to check if the device
# is within range and ready for communication.
# If device is never found, it WILL run forever.
#######################################################
def connection_checks(mac):
    checks = []
    while len(checks) < 3:
        # Device WAS found during scan
        if within_range(mac):
            checks.append("PASS")
            print("Found device! [PASS {}] <(^.^)>".format(len(checks)))

        # Device was NOT found during scan
        else:
            check = []
            print("Device not found! [Failure] <(-.-)>")

    return True

############################################################
# Name: connect
# Desc: Attempts to connect to the peripheral.
############################################################
def connect(peripheral, mac, addr_type):
    try:
        print("Attempting to connect to device...")
        peripheral.connect(mac, addr_type)
        print("Connection successful!")
    except BTLEException as e:
        print(e)

############################################################
# Name: disconnect
# Desc: Attempts to disconnect form the peripheral.
############################################################
def disconnect(peripheral):
    try:
        print("Disconnecting from device...")
        peripheral.disconnect()
        print("Disconnection successful!")
    except BTLEException as e:
        print(e)

############################################################
# Name: notifications_on
# Desc: Writes the "on" code to the CCCD to allow for 
# notifications to be asyncrhonously processed. 
############################################################
def notifications_on(peripheral, uuid):
    setup_data = "\x01\x00".encode()
    notify = peripheral.getCharacteristics(uuid=uuid)[0]
    notify_handle = notify.getHandle() + 1
    peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)

############################################################
# Name: notifications_off
# Desc: Write the "off" code to the CCCD to turn off
# asynchronous notifications. (Not currently used)
############################################################
def notifications_off(peripheral, uuid):
    setup_data = "\x00\x00".encode()
    notify = peripheral.getCharacteristics(uuid=uuid)[0]
    notify_handle = notify.getHandle() + 1
    peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)

###########################################################
# Name: write_fileno
# Desc: Writes the file number to a file for persistant
# storage.
###########################################################
def write_fileno(path,fileno):
    with open(path, "w+") as f:
        f.write(fileno)

###########################################################
# Name: read_fileno
# Desc: Reads the file number from a file for persistant
# storage.
###########################################################
def read_fileno(path):
    with open(path, "r") as f:
        fileno = f.read()
        
        # In the event nothing was read, start over
        if(fileno == ""):
            fileno = 1

    return fileno

###########################################################
# Name: fileno_parse
# Desc: Takes the last few strings received from the 
# peripheral and attempts to parse out the file number.
###########################################################
def fileno_parse(string):
    try:
        # Remove all newline characters 
        nn = string.replace("\n", "")

        # Split string by comma's
        ss = nn.split(",")

        # Grab fileno
        fn = ss[-2]
    except IndexError as e:
        print(e)

    return fn

###########################################################
# Name: fcode
# Desc: String formatter to specify how many letters the
# BLE connection will be sending to the activity monitor.
# This is a bluepy independent format.
# < - little endian, {} - string length, s - string
###########################################################
def fcode(string):
    l = len(string)
    s = "<{}s".format(l)

    return s


############################################################
# Name: send_command
# Desc: Writes a command to the peripheral. It takes the
# command argument and gathers the format code and byte
# representation in order to properly execute the given
# command to the peripheral.
############################################################
def send_command(peripheral, uuid, cmd): 
    dc = fcode(cmd)
    d = cmd.encode()

    # Pack information
    p = pack(dc, d)

    # Send to device
    c = peripheral.getCharacteristics(uuid=uuid)[0]
    c.write(p)

############################################################
# Name: receive_data
# Desc: Receives data from the peripheral. Returns it as a
# list. 
############################################################
def receive_data(peripheral, notification):
    data = []
    msg = ""

    try:
        while True:
            if actimo.waitForNotifications(1.0):
                # handleNotification() was called
                msg = notification.get_message()
                data.append(msg)
                print(msg)
                
                # "!!!" represents end of transfer
                if "!" in msg:
                    break
                
                continue

    except BTLEException as e:
        print(e)
        
    return data

############################################################
# Name: set_time
# Desc: Grabs the current date/time, formats it, sends it
# to the peripheral.
############################################################
def set_time(peripheral, uuid):
    dt = datetime.now().strftime("%Y,%m,%d,%H,%M,%S")
    send_command(actimo, uuid, "settime,")
    time.sleep(1) # necessary, the Pi may be to fast. 
    send_command(actimo, uuid, dt)

##########################################################
### Main Module ##########################################
##########################################################
if __name__ == "__main__":

    ACTIVITY_MAC =      "f2:3f:39:f8:4d:35"
    ADDRESS_TYPE =      "random"
    SERVICE_UUID =      "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    WRITE_CHAR_UUID =   "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    READ_CHAR_UUID  =   "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    FILENO_PATH =       "/home/pi/Activity_Monitor_Base_Station/base_station/fileno.txt"



    # Box Setup
    bx = Box()

    ################
    # Control Loop #
    ################
    while True:
        
        # Peripheral object
        actimo = Peripheral(None)

        # Asynchronous notification setup
        nd = NotificationDelegate(DefaultDelegate)
        actimo.setDelegate(nd)
        
        # Wait until peripheral is ready
        connection_checks(ACTIVITY_MAC)    

        # Connect to peripheral
        connect(actimo, ACTIVITY_MAC, ADDRESS_TYPE)

        # Acquire last file number read from peripheral
        fn = read_fileno(FILENO_PATH)

        # Update peripheral with new time stamp
        set_time(actimo, WRITE_CHAR_UUID)
        time.sleep(1)

        # Turn peripheral notifications on
        notifications_on(actimo, READ_CHAR_UUID)

        # Begin communication, starting from specified file number
        send_command(actimo, WRITE_CHAR_UUID, "comm,{},".format(fn))

        # Read in all data until 'end' command is read
        data = receive_data(actimo, nd)
        
        # Disconnect from peripheral
        disconnect(actimo)
        
        # Update file number 
        if len(data) > 1:
            print("ENTER ENTER ENTER")
            write_fileno(FILENO_PATH, fileno_parse("".join(data[-2:])))
        
            # Write all received information to a file
            bx.write_to_file("".join(data))
            
            # Upload file to Box
            bx.upload_file()

        # Sleep cycle to allow peripheral to collect data
        print("Entering sleep cycle. <(~.~)>")

        # Delay to collect more data
        time.sleep(120)
