# Activity_Monitor_Base_Station
A Bluetooth Low Energy (BLE) project that acts as the BLE central for communication with a BLE peripheral device.
The core focus of the base station is to initiate and handle all forms of communication to transfer data gathered
from the peripheral device. It acts a relay of sorts, receiving data from the periphal, temporarily storing it, and
then uploading it to a cloud service provider for long term storage. It allows for rather large data transfers
from the periphal to the central, all the while ensuring there is little to no packet loss, at speeds that reach 
close to the theoretical maximum throughput of BLE 4.2.

### Prerequisites
**BLE Central:** Raspberry Pi Model 3 B+, a monitor with hdmi port, hdmi cable, keyboard, internet, usb power supply and sd card.  
    
**BLE Peripheral:** Nordic SemiConductor NRF52840 dev board  
  
### Installing
1) Download[Raspbian Stretch Lite](https://www.raspberrypi.org/downloads/raspbian/) operating system (OS) for the Pi.
  
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
  
7) The following is basic configuration setup for the Pi...  
```
sudo raspi-config  
```
**Locale Setup**
Central U.S.A. setup, may be different depending on your location...  
Choose *Localisation Options* -> *Change Locale* -> uncheck *en_GB.UTF-8 UTF-* -> check *en_US.UTF-8 UTF-8.  
Choose *Localisation Options* -> *Change Timezone* -> choose *US* -> *Central*  
You will want to edit the file /etc/default/keyboard and change the *XKBLAYOUT="gb"* to *XKBLAYOUT="us"*  
You can now reboot, ```sudo reboot```  

**Network Setup**
If you are plugged in directly via an ethernet cable, you can skip the following *Network Setup* guide. 
This section covers a very brief basic setup of connecting to your wifi via the Pi.
Choose *Network Options* -> *Wi-fi* -> proceed to enter your networks name and password.  
You can test your connection via...
```
ping google.com
```  
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
	identity="blahblah@blah.com"
	password="secretsecret"
	phase1="peapver=0"
	phase2="MSCHAPV2"
}
```
  
8) With the network now setup, we can run the following to ensure the Pi and it's repositories are up to date.  
```
sudo apt-get update
sudo apt-get upgrade
```
  
9) 





