from bluepy.btle import DefaultDelegate

class NotificationDelegate(DefaultDelegate):

    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.msg = ""

    # The asynchronous handler, should it encounter
    # a special character, simply ignore that msg. 
    def handleNotification(self, cHandle, data):
        try:
            self.msg = data.strip().decode()
        except UnicodeDecodeError as e:
            self.msg += "\nError: Special character encountered!"   
            #print(e)

    def get_message(self):
        return self.msg

