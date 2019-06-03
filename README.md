# Activity_Monitor_Base_Station
A Bluetooth Low Energy (BLE) project that acts as the BLE central for communication with a BLE peripheral device.
The core focus of the base station is to initiate and handle all forms of communication to transfer data gathered
from the peripheral device. It acts a relay of sorts, receiving data from the periphal, temporarily storing it, and
then uploading it to a cloud service provider for long term storage. It allows for rather large data transfers
from the periphal to the central, all the while ensuring there is little to no packet loss, at speeds that reach 
close to the theoretical maximum throughput of BLE 4.2.

### Prerequisites
**BLE Central:** Raspberry Pi Model 3 B+, a monitor with hdmi port, hdmi cable, keyboard, internet, usb power supply and sd card. A decent understanding of Linux and it's command line features. This guide does not assume your an expert, but you must be familiar at the very least with command line text editing, running programs, installing packages, .  
    
**BLE Peripheral:** Nordic SemiConductor NRF52840 dev board. While this project focuses specifically on the NRF52840 chip, it can be generalized to really any BLE peripheral. This guide assumes you have a decent understanding of how BLE works, what a characteristic, service, packet etc means. For more information check out this useful guide found [here](https://www.novelbits.io/basics-bluetooth-low-energy/). There are multitudes of great guides online, I had to read through several myself before really understanding how BLE works.  
  
### Installing
1) Download [Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) operating system (OS) for the Pi.
  
2) You then will need to grab [Etcher](https://www.balena.io/etcher/) which will allow to you flash the OS onto the Pi.  
*Verify the SHA-256 checksum matches*  
  
3) Run Etcher, and proceed to flash the newly downloaded Raspbian OS onto the Pi's SD card.  
*Your SD card will need to be connected to your main computer, via an SD card reader or a USB to SD card holder*
  
4) Once Etcher has completed, you may now remove the card and plug it back into the Pi.
  *Etcher can take a while to complete*  
  
5) Set up the Pi to be connected to a monitor via HDMI cable, insert sd card, plug in keyboard, and then proceed to plug in the power supply, from which point the Pi will automatically boot.  
*You are now booted into the Pi directly to the 'command line'*
  
6) Proceed to enter the default user name and password
```
login:pi  
password: raspberry  
```
  
7) The following is basic configuration setup for the Pi  
  
**Automatic Login Setup**
```
sudo raspi-config  
```  
On boot, the Pi will automatically log us in without user name or password.  
Choose *Boot Options* -> *Desktop / CLI* -> *Console Autologin* 

**SSH Setup**  
```
sudo raspi-config  
```  
This will allow us to later on configure SSH to remotely boot into the Pi.  
Choose *Interfacing Options* -> *SSH* -> *YES!*  
  
**Locale Setup**
```
sudo raspi-config  
```  
Central U.S.A. setup, may be different depending on your location...  
Choose *Localisation Options* -> *Change Locale* -> uncheck *en_GB.UTF-8 UTF-* -> check *en_US.UTF-8 UTF-8.  
Choose *Localisation Options* -> *Change Timezone* -> choose *US* -> *Central*  
You will want to edit the file /etc/default/keyboard and change the *XKBLAYOUT="gb"* to *XKBLAYOUT="us"*  
You can now reboot,  
```sudo reboot```  

**Network Setup**
```
sudo raspi-config  
```  
If you are plugged in directly via an ethernet cable, you can skip the following *Network Setup* guide. 
This section covers a very brief basic setup of connecting to your wifi via the Pi.
Choose *Network Options* -> *Wi-fi* -> proceed to enter your networks name and password.  
You can test your connection via...  
```ping google.com```  
  
In some situations this may not work entirely depending on your network setup, in which case you will have to do some digging on your own. In my case, I'm on a public college network that requires a username and password. You can add the following file to /etc/wpa_supplicant/wpa_supplicant.conf, you will need to use the ```nano``` text editor to make changes for which there a multiple guides online how to use.  
```
ctrl_interface=/run/wpa_supplicant.conf GROUP=netdev
update_config=1
country=US
network={
	ssid="yournetworkname"
	scan_ssid=1
	key_mgmt=WPA-EAP
	pariwise=CCMP TKIP
 group=CCMP TKIP
	eap=PEAP
	identity="yourusername"
	password="secretsecret"
	phase1="peapver=0"
	phase2="MSCHAPV2"
}
```
At this point it's a good idea to reboot the system to allow all the changes to take effect, in doing so, you should automatically connect to the wifi as well.
```sudo reboot```
  
8) With the network now setup, we can run the following to ensure the Pi and it's repositories are up to date.  
*This can take a while...*
```
sudo apt-get update
sudo apt-get upgrade
```
  
9) With the Pi now connected to the internet we can look into setting up the remote connection via SSH. The remote connection will 
allow us to remove the need for a stand alone keyboard, monitor, hdmi cable, etc and will allow it to connect remotely through a program called Putty. Please not using this method, it is possible that there is a static ip name collision, in which case you will have to try a few different values for *static ip_address* found below...

We will first need gather some information on the Raspberry Pi side.  
**Value1:** If you are using wifi, this value will be *wlan0*, if you are using ethernet, this value will be *eth0*  
**Value2:** ```ip -4 addr show | grep``` Take note of the IP address and network size, something like 10.12.18.255/16  
**Value3:** ```ip route | grep default | awk '{print $3}'``` Take note of address of your router/gateway, something like 10.12.255.255  
**Value4:** ```cat /etc/resolv.conf``` Take note of the nameserver value, something like 137.48.1.255  
  
Now we need to edit the file /etc/dhcpcd.conf  
```nano /etc/dhcpcd.conf```  
And then add the following, substituting the values found above into there respected locations marked below.  
```
Here is an example which configures a static address, routes and dns.
       interface Value1
       static ip_address=Value2
       static routers=Value3
       static domain_name_servers=Value4
```  
At this point we now have a static ip address, that is independent of whatever network we are connected. Without this step, it is possible that the Pi's ip address could change each time we connect to a network. It is now a good idea to try and use Putty to connect to the Pi remotely before proceeding.  
* First you will need to download [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html) on your local computer.
* In the Host Name field, enter the ip address we found from above. (Value2, without the /16 at the end, 10.12.18.255 for instance)
* Click open, agree to the popup and proceed to log in using the default login.
  
We can now begin setting up the public and private keys for automatic login, while maintaining a high level of security. To begin we will need to generate a public and private key pair. 
* PuTTy comes with a program called PuttyGen which will generate our public and private key pairs. Start it up and click on generate. Moving your mouse to generate entropy. Save both the public and private keys somewhere you will remember. 
* Now on the pi do the following...
```
cd /home/pi  
mkdir .ssh
sudo chmod 700 .ssh
```
* Using a program such as [WinSCP](https://winscp.net/eng/index.php) you can remotely transfer files using the same ip address we used to log in with PuTTy. So transfer **ONLY** the public key to the newly created .ssh directory. Once the new public key is transferred, run the following...
```
sudo chmod 700 public
mv public authorized_keys
```
* Now you can fire up PuTTY, input the IP address we used earlier into the Host Name field. 
* On the left hand side choose *SSH* -> *Auth* -> and in the private key field, browse for your newly created private key file.
* Back in the *Session* tab, be sure to give the *Saved Session* a name, and then hit *Save* before proceeding to connect. This will save you in the future from having to go update those values.
* Go ahead and try to connect now. Once you enter your username it should automatically log you in. If you happen to get a "server refused our key" message check out this article located [here](http://www.walkernews.net/2009/03/22/how-to-fix-server-refused-our-key-error-that-caused-by-putty-generated-rsa-public-key/) to properly format the file.  
  
10) We will now install a few needed pieces of software on the Pi to allow us to build the actual project.  
```
sudo apt-get install git python3-pip libglib2.0-dev  
sudo pip3 install bluepy
sudo pip3 install boxsdk
sudo pip3 install boxsdk[jwt]
```  
 This will install all packages needed to run the base station code. 
  
11) We can now pull in the code base from GitHub by issuing the following...
```
cd /home/pi
git clone https://github.com/unomachineshop/Activity_Monitor_Base_Station.git
```  

12) A single file is left missing that contains sensitive information in regards to being able to log into the Box SDk for long term storage. You will need to accomplish a few things though before we add that file.  
* First, create an account at [Box](https://www.box.com/home)
* You will then need to follow the directions [here](https://developer.box.com/docs/setting-up-a-jwt-app) which will allow you to set up an application which gives you access to an API key amongst other security parameters. Follow the guide with the mindest of setting up the JWT authentication, as JWT allows automatic refreshes on your client token.   
* You will eventually get to a point where you end up downloading a config file that is automatically generated based upon the criteria you set up through that guide. Ensure that file is named *config.json*. You need to then transfer this file to your Pi via WinSCP or some other file transfer method. You will need to move it to the directory */home/pi/Activity_Monitor_Base_Station/box*  
* You will end up with a file similair to this, (Obviously all the data values have been changed for security reasons, but this is to give you an idea of what you should end up with.)
```
{
  "boxAppSettings": {
    "clientID": "alphanumeric567345",
    "clientSecret": "alphanumeric345345",
    "appAuth": {
      "publicKeyID": "alphanumeric123123",
      "privateKey": "-----BEGIN ENCRYPTED PRIVATE KEY-----\nblahsecretdigits1-08fasd0f-98asdf0af-8a7sfd-8a7s89v-a8df7as8df-0as8fd7u-\nFSI=\n-----END ENCRYPTED PRIVATE KEY-----\n",
      "passphrase": "blahsecretdigits123123aesrf3"
    }
  },
  "enterpriseID": "digits0a8134"
}
```
* Lastly you will need to programatically set up a folder, which will be viewable, and located within the *admin console -> content* view on the Box dashboard. This folder will be where the data gets uploaded to, and is shareable through Box's GUI setup. The folder will be named *Activity_Monitor*. It's very similair to how you would share any file or folder on Box with someone else. The only exception being you must programmatically set it up, through the Python interpreter. *Make sure to only run the following only once!.*
```
cd /home/pi/Activity_Monitor_Base_Station/box
python3
import box
b = box.Box()
b.create_box_folder()
```  
After running these commands you will see one of two messages. *Success* indicates the folder was created and is now viewable through the Box *admin console*. *Failed* indicates there was an issue, perhaps with your wifi, the previous steps, or perhaps there already exists a folder named "Activity_Monitor". For more information on the Box API please check out the following, [Box Guide](https://developer.box.com/reference)

13) Now you can successfully run the program manually by issuing the following...  
```sudo python3 /home/pi/Activity_Monitor_Base_Station/base_station/blue.py```
It will run through a series a checks and then begin to attempt to read data from the peripheral device. While this is nice, we have set up a way to completely automate this on boot. Before proceeding it is definitely worth it to try and run this manually, to ensure that all the work up to this point is correct.  
  
14) You may have noticed when navigating through the directories that there was a file highlighted green called forever.py. This file is used in conjunction with Linux's cron job scheduler to ensure that blue.py will run forever. The program could crash, lose power, etc, and this script will ensure that no matter what, blue.py attempts to stay alive. The set up is simple...  
```sudo crontab -e``` this opens up the super user's crontab page. (Needed for BLE scanning)  
Then add the following anywhere in the file...  
```@reboot python3 cd /home/pi/Activity_Monitor_Base_Station && /home/pi/Activity_Monitor_Base_Station/forever.py```   
*Please note, you must add the cd command, because crontab will start up in the user's home directory, which can cause conflicts due to pathing*
  
15) At this point you can simply reboot the Pi, and the code will automatically start, and will continue to run as long as the Pi has power to it. Since everything gets handled in the background, the easiest way to check output is through Box's admin console. Once a full iteration of communication is complete, the base station will upload the transfered data directly to Box, through the folder we created above. To view this go to *[Box.com](box.com)* -> *login* -> on the left hand side click *admin console* -> *content* -> search for the folder named *Activity_Monitoring* and you will see all previous uploaded files to that folder. The naming conventing is a simple date/time string, derived from the exact instance the file was uploaded.  
*Should you have trouble with the autostart feature, you can run the program ```htop``` look for the running script, take note of it's process id, and then run the following ```sudo strace -pXXX -s9999 -e write``` where XXX is the given process id.*
  
16) The code is fully commented and very self explanatory. I would recommend reading through all of it, starting with blue.py to get a better understanding of how the lifecycle of this program works. If you don't feel like reading through the code, you can always check on the Box folder, and refresh it every now and again to view the updated information.   
  
**Thanks for reading!**



