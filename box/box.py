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
        self.FILE_ERROR_PATH =  "/home/pi/Activity_Monitor_Base_Station/box/error.txt"
        
        # Remote
        self.DATA_FOLDER =    "75253867312" # CHANGE THIS
        self.ERROR_FOLDER =   "78605578754" # CHANGE THIS
        self.client = ""
        
        # Retrieve authentication information from config file
        auth = JWTAuth.from_settings_file(self.CONFIG_PATH)
        # Authenticate applications token
        access_token = auth.authenticate_instance()
        # Authorize application client
        self.client = Client(auth)
        
    #########################################################
    # Name: write_data_to_file
    # Desc: Writes a transfered peripheral data to a file.
    #########################################################
    def write_data_to_file(self, data):
        try:
            with open(self.FILE_WRITE_PATH, 'w') as f:
                f.write(data)
        except IOError as e:
            print(e)

    #######################################################
    # Name: write_error_to_file
    # Desc: Writes error data to file
    #######################################################
    def write_error_to_file(self, error):
        try:
            with open(self.FILE_ERROR_PATH, 'a') as f:
                dt = datetime.now().strftime("%Y-%m-%d %H:%M:%S  ") 
                f.write(dt + repr(error) + "\n")
        except IOError as e:
            print(e)

    #########################################################
    # Name: create_box_folder
    # Desc: Creates a folder that is then shared with other
    # people who need access. Upon folder creation, you must
    # manually go to admin panel > content > share, and 
    # specifiy the email address of whoever needs access.
    #########################################################
    def create_box_folder(self, folder_name):
        #folder_name = "Activity_Data"
        folder_id = 0 # Root level
        try:
            folder = self.client.folder(folder_id).create_subfolder(folder_name)
            print("Folder ID:" +  folder.id)
        except BoxAPIException as e:
            print(e)
            print("Failed to create box folder, check internet connection, and ensure folder wasn't already created!")

    #########################################################
    # Name: upload_data_file
    # Desc: Uploads an entire data file to Box. Uploads are
    # dependent upon communication iterations.
    #########################################################
    def upload_data_file(self):
        file_name = datetime.now().strftime("%Y-%m-%d_%H:%M:%S") + ".txt"
        try:
            box_file = self.client.folder(self.DATA_FOLDER).upload(self.FILE_WRITE_PATH, file_name, preflight_check=True)
        except BoxAPIException as e:
            print(e)

    #######################################################
    # Name: upload_error_file
    # Desc: Uploads an entire error file to Box. Uploads 
    # are done daily, via a cronjob.
    #######################################################
    def upload_error_file(self):
        file_name = datetime.now().strftime("%Y-%m-%d") + ".txt"
        try:
            box_file = self.client.folder(self.ERROR_FOLDER).upload(self.FILE_ERROR_PATH, file_name, preflight_check=True)
        except BoxAPIException as e:
            print(e)

    ########################################################
    # Name: error_file_clear
    # Desc: Clears the contents of the error file, executed
    # after the error file has been uploaded. 
    #######################################################
    def error_file_clear(self):
        open(self.FILE_ERROR_PATH, 'w').close()
