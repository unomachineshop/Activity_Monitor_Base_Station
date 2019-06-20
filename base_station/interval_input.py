import re

INTERVAL_PATH = "/home/pi/Activity_Monitor_Base_Station/base_station/interval.txt"

while True:
    #Get user input
    values = input("Please enter 10 integers seperated by commas with no whitespace: ")
    # Remove leading and trailing whitespace
    values = values.strip()
    # Split by comma
    l = values.split(",")
    
    # Simple format check
    if(len(l) == 10 and " " not in values):
        try:
            with open(INTERVAL_PATH, 'w') as f:
                f.write(values)
                print("\nSuccessfully updated the 10 integer interval!\n\nIn order for the changes to take effect, please reset the Base Station!")
                break
        except IOError as e:
            print(e)

    # Input failed to meet criteria
    print("Invalid format")
