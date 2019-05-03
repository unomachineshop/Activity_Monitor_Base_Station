import binascii
import struct
import time
from struct import *
from datetime import datetime
from bluepy.btle import DefaultDelegate, Peripheral, Scanner
from collections import OrderedDict

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

    print("Device wasn't found...")
    return False

############################################################
# Name: connect
# Desc: Attempts to connect to the peripheral.
############################################################
def connect(peripheral, mac, addr_type):
    try:
        print("Attempting to connect to device...")
        peripheral.connect(mac, addr_type)
        print("Connection successful!")
    except BTLEExcpetion as e:
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
# asynchronous notifications.
############################################################
def notifications_off(peripheral, uuid):
    setup_data = "\x00\x00".encode()
    notify = peripheral.getCharacteristics(uuid=uuid)[0]
    notify_handle = notify.getHandle() + 1
    peripheral.writeCharacteristic(notify_handle, setup_data, withResponse=True)

###########################################################
# Name: write_fileno
# Desc: 
###########################################################
def write_fileno(fileno):
    with open("fileno.txt", "w+") as file:
        file.write(fileno)

###########################################################
# Name: read_fileno
# Desc: 
###########################################################
def read_fileno():
    with open("fileno.txt", "r") as file:
        fileno = file.read()

    return fileno

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
# Desc: Receives data from the peripheral. 
############################################################
def receive_data(peripheral, notification):
    data = []
    #data = ""
    msg = ""

    try:
        while "end" not in msg:
            if actimo.waitForNotifications(1.0):
                # handleNotification() was called
                msg = notification.get_message()
                #data += msg
                data.append(msg)
                if("file" in msg):
                    print(msg)
                #print(msg)
                continue

    except BTLEException as e:
        print(e)

    
    return ''.join(data)
    
############################################################
# Name: set_time
# Desc:
############################################################
def set_time(peripheral, uuid):
    #send_command(actimo, uuid, fcode("settime"), b"settime")
    dt = datetime.now().strftime("%Y,%m,%d,%H,%M,%S")

    send_command(actimo, uuid, "settime,")
    time.sleep(.5) # necessary, the Pi may be to fast. 
    send_command(actimo, uuid, dt)
    
###########################################################
# Name: get_time
# Desc: 
###########################################################
def get_time(peripheral, notification):
    send_command(actimo, WRITE_CHAR_UUID, "gettime") 
    notifications_on(actimo, READ_CHAR_UUID)
    receive_data(actimo, nd) # Might go before send command
    notifications_off(actimo, READ_CHAR_UUID)

###########################################################
# Name: stop
# Desc: 
###########################################################
def stop(peripheral, uuid):
    send_command(actimo, uuid, "stop")



##########################################################
### Main Module ##########################################
##########################################################
if __name__ == "__main__":

    #ACTIVITY_MAC =      "ec:01:25:f5:3d:b4"
    ACTIVITY_MAC =      "f2:3f:39:f8:4d:35"

    ADDRESS_TYPE =      "random"
    SERVICE_UUID =      "6e400001-b5a3-f393-e0a9-e50e24dcca9e"
    WRITE_CHAR_UUID =   "6e400002-b5a3-f393-e0a9-e50e24dcca9e"
    READ_CHAR_UUID  =   "6e400003-b5a3-f393-e0a9-e50e24dcca9e"

    # Activity Monitor setup
    actimo = Peripheral(None)
    nd = NotificationDelegate(DefaultDelegate)
    actimo.setDelegate(nd) 
    
    # Box Setup
    #bx = Box()
    #bx.connect_to_box()
   

    """
    # Breakage testing for forever.py and crontab -e
    while(True):
        print("Alive")
        time.sleep(10)
        print("Dead")
        s = 10 / 0
        time.sleep(1)
    """


    
    ###############################################
    #### Testing ##################################
    ###############################################
    # Connecting to device
    
    connect(actimo, ACTIVITY_MAC, ADDRESS_TYPE)

    # Good!
    #send_command(actimo, WRITE_CHAR_UUID, "comm,20")
    
    #notifications_on(actimo, READ_CHAR_UUID)
    
    #x = receive_data(actimo, nd)
    #notifications_off(actimo, WRITE_CHAR_UUID)
    
    #Good!
    #set_time(actimo, WRITE_CHAR_UUID)

    # Disconnect device
    disconnect(actimo)
    

    """
    # Success
    write_fileno("10")
    print(read_fileno())

    write_fileno("13")
    print(read_fileno())
    """


    #bx.connect_to_box()
    #bx.write_to_file(x)
    #bx.upload_file() 
    
    #send_data(actimo, nd, WRITE_CHAR_UUID, READ_CHAR_UUID)
    #bx.upload_file()
    #set_time(actimo, WRITE_CHAR_UUID)
    #stop(actimo, WRITE_CHAR_UUID)
   ###############################################
