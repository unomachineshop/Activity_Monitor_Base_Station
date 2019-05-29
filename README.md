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
**Automatic Login Setup**  
On boot, the Pi will automatically log us in without user name or password.  
Choose *Boot Options* -> *Desktop / CLI* -> *Console Autologin* 

**SSH Setup**  
This will allow us to later on configure SSH to remotely boot into the Pi.
Choose *Interfacing Options* -> *SSH* -> *YES!*  
  
**Locale Setup**
Central U.S.A. setup, may be different depending on your location...  
Choose *Localisation Options* -> *Change Locale* -> uncheck *en_GB.UTF-8 UTF-* -> check *en_US.UTF-8 UTF-8.  
Choose *Localisation Options* -> *Change Timezone* -> choose *US* -> *Central*  
You will want to edit the file /etc/default/keyboard and change the *XKBLAYOUT="gb"* to *XKBLAYOUT="us"*  
You can now reboot,  
```sudo reboot```  

**Network Setup**
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
At this point it's a good idea to reboot the system to allow all the changes to take effect, including automatically connecting to the wifi.  
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
**Value2:** ```ip -4 addr show | grep``` Take note of the IP address and network size, for example something like 10.12.18.255/16  
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
At this point we now have a static ip address, that is independent of whatever network we are connected. Without this step, it is possible that the Pi's ip address could change each time we connect to a network. It is now a good idea to try and use Putty to connect to the Pi remotely before proceeding to the next steps.  
* First you will need to download [PuTTY](https://www.chiark.greenend.org.uk/~sgtatham/putty/latest.html)
* In the Host Name field, enter the ip address we found from above. (Value2, without the /16 at the end, 10.12.18.255 for instance)
* Click open, agree to the popup and proceed to log in using the default login.
  
We can now begin setting up the public and private keys for automatic login, while maintaining a high level of security. To begin we will need to generate a public and private key pair. 
* On the Pi run the command ```ssh-keygen```, and just hit enter through the default questions, no password needed. This command will generate your public (id_rsa.pub) and private key (id.rsa) pairs to the directory /home/pi/.ssh.  
* The public key (id_rsa.pub) will stay on the Pi...
```mv id_rsa.pub authorized_keys```  Name change for default SSH configuration
```sudo chmod 400 authorized_keys``` Permission change (read only)
* The private key (id_rsa) will need to be relocated to somehwere on your desktop. In order to move the file, you can mount a USB drive to the Pi and manually transfer it, or you can use a program such as [WinSCP](https://winscp.net/eng/index.php) to remotely transfer files. WinSCP uses the same exact ip address that we used for PuTTy. Either way way will work, just make note of where you saved the file on your local machine.  
* Once the private key is transferred, fire up PuTTy. On the left hand side expand *SSH* and then click on *Auth*. 
* Browse for your newly transferred private key and select it. Now back in the *Session* tab, simply input your ip address again









