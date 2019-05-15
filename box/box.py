from boxsdk import Client, JWTAuth, BoxAPIException
from datetime import datetime

class Box():
    
    #########################################################
    # Name: __init__
    # Desc: Basic initialization of local and remote pathing 
    # variables. 
    #########################################################
    def __init__(self):
        # Local
        self.CONFIG_PATH =      "/home/pi/Activity_Monitor_Base_Station/box/config.json"
        self.FILE_READ_PATH =   "/home/pi/Activity_Monitor_Base_Station/box/read.txt"
        self.FILE_WRITE_PATH =  "/home/pi/Activity_Monitor_Base_Station/box/write.txt"
        
        # Remote
        self.SHARED_FOLDER =    "75253867312" # Activity Monitor folderid
        self.client = ""
        
        # Retrieve authentication information from config file
        auth = JWTAuth.from_settings_file(self.CONFIG_PATH)
        # Authenticate applications token
        access_token = auth.authenticate_instance()
        # Authorize application client
        self.client = Client(auth)
        


    ## MAY REMOVE THIS
    #########################################################
    # Name: connect_to_box
    # Desc: Sets up authentication via JWT access tokens to
    # the enterprise application. This approach allows the 
    # script to always get authenticated automatically. 
    #########################################################
    def connect_to_box(self):
        # Retrieve authentication information from config file
        auth = JWTAuth.from_settings_file(self.CONFIG_PATH)
        # Authenticate applications token
        access_token = auth.authenticate_instance()
        # Authorize application client
        self.client = Client(auth)
  
    #########################################################
    # Name: write_to_file
    # Desc: Writes a chunk of data to a file.
    #########################################################
    def write_to_file(self, data):
        try:
            with open(self.FILE_WRITE_PATH, 'w') as file:
                file.write(data)
        except IOError as e:
            print(e)

    #########################################################
    # Name: create_box_folder
    # Desc: Creates a folder that is then shared with other
    # people who need access. Upon folder creation, you must
    # manually go to admin panel > content > share, and 
    # specifiy the email address of whoever needs access.
    #########################################################
    def create_box_folder(self, parent_id, folder_name):
        #folder_name = "Activity Data"
        #folder_id = 0 # Root level
        try:
            folder = self.client.folder(folder_id=parent_id).create_subfolder(folder_name)
            return True
        except BoxAPIException as e:
            print(e)

        print(folder)
        return False

    #########################################################
    # Name: upload_file
    # Desc: Uploads a  file under the shared folder, which
    # uses a datetime naming convention.
    #########################################################
    def upload_file(self):
        file_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
        try:
            box_file = self.client.folder(self.SHARED_FOLDER).upload(self.FILE_WRITE_PATH, file_name, preflight_check=True)
            return True
        except BoxAPIException as e:
            print(e)
        
        return False


### Test Code ###
#b = Box()
#b.connect_to_box()
#b.create_box_folder(0, "Activity Data")
#b.upload_file()

