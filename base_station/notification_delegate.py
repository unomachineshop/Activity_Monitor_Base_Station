from bluepy.btle import DefaultDelegate

class NotificationDelegate(DefaultDelegate):

    def __init__(self, params):
        DefaultDelegate.__init__(self)
        self.msg = ""

    def handleNotification(self, cHandle, data):
        self.msg = data.strip().decode()

    def get_message(self):
        return self.msg

