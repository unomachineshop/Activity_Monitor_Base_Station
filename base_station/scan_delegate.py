from bluepy.btle import DefaultDelegate

class ScanDelegate(DefaultDelegate):
    
    #######################################################
    # Name: __init___
    # Desc: Initializes Bluepy's Default Delegate class.
    #######################################################
    def __init__(self):
        DefaultDelegate.__init__(self)

    #######################################################
    # Name: HandleDiscovery
    # Desc: Asynchronous call that receives scannning
    # information. Newly found devices and new data
    # automatically populate when they are received.
    #######################################################
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            pass
            #print("Discovered device", dev.addr)
        elif isNewData:
            pass
            #print("Received new data from", dev.addr)

