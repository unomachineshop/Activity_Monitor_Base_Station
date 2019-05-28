# Activity_Monitor_Base_Station
A Bluetooth Low Energy (BLE) project that acts as the BLE central for communication with a BLE peripheral device.
The core focus of the base station is to initiate and handle all forms of communication to transfer data gathered
from the peripheral device. It acts a relay of sorts, receiving data from the periphal, temporarily storing it, and
then uploading it to a cloud service provider for long term storage. It allows for rather large data transfers
from the periphal to the central, all the while ensuring there is little to no packet loss, at speeds that reach 
close to the theoretical maximum throughput of BLE 4.2.

### Prerequisites
In order to run this project, you will need several components consisiting of both hardware and software.  
  **BLE Central:** Raspberry Pi Model 3 B+  
  **BLE Peripheral:** Nordic SemiConductor NRF52840 dev board   
  **Storage:** A box account  

