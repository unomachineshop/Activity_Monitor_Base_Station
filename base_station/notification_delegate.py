from bluepy.btle import DefaultDelegate

class NotificationDelegate(DefaultDelegate):

    #######################################################
    # Name: __init__
    # Desc: Initializes bluepy's Default Delegate and the
    # message string.
    #######################################################
    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.msg = ""

    #######################################################
    # Name: handleNotification
    # Desc: Asynchronous call that will handle the 
    # notifications recieved from the peripheral.
    #######################################################
    def handleNotification(self, cHandle, data):
        try:
            self.msg = data.strip().decode()
        except UnicodeDecodeError as e:
            self.msg += "\nError: Special character encountered!"   
            #print(e)

    #######################################################
    # Name: get_message
    # Desc: Helper method to acquire newly recieved 
    # message.
    #######################################################
    def get_message(self):
        return self.msg

