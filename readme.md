# Domoticz-Jeelink-Plugin



Python plugin to use with Jeelink and Jeenodes

## Key Features

- Creates and updates Domoticz Devices defined by the user and sended over Jeenode

- Example :

   - 1 PAPP </br>
     2. ...


  Keys must be adapted to your Parameter in the onStart() parts. See configuration.

## Installation

Tested on Python version 3.5.3  & Domoticz version 4.10717 .

To install:

- Go in your Domoticz directory, 	open the plugins directory.  	
- Navigate to the directory using 	a command line  	
- Run: `git 	clone 	https://github.com/moustache13/DOMOTICZ-python-PLUGIN-for-Jeelink-and-Jeenodes`
- Restart Domoticz.  	

In the web UI, navigate to the Hardware page. In the hardware dropdown there will be an entry called "Jeelink".

## Updating

To update:

- Go in your Domoticz directory 	using a command line and open the plugins directory then the 	Domoticz-Jeelink-Plugin directory.  	
- Run: `git 	pull`  	
- Restart Domoticz.  	

## Configuration

| Field          | Information                                                  |
| -------------- | :----------------------------------------------------------- |
| Serial Port    | Dropdown to select the Serial Port the Jeelink is plugged into |
| Debug          | When true the logging level will be much higher to aid with troubleshooting, when set to 'Logging' a 'plugin.log' file will be created in the plugin folder with debug information |
| Create Devices | You must adapt the list of devices in the plugin.py file  				 		       		          **onStart()** <br/>if (len(Devices) == 0):  				 				           <br/>Domoticz.Device(Name="JeelinkAllData", Unit=1, TypeName="Usage").Create() |
| Update Devices | update the array index in in the plugin.py file  				 			<br/>**onMessage()** 				<br/>isValue = str(int(bytesLineSplitted[2])) 				<br/>Devices[1].Update(nValue=0, sValue=isValue, TimedOut=0) |

## Configuration Jeenode

**Net group**

The net group in Jeenode and Jeelink must be the same (default 100)

**Node ID**

The Node ID of the Jeenode must be 1 … 9

https://jeelabs.org/2011/01/14/nodes-addresses-and-interference/  

## Format of message  sended by the Jeenode :

blank Label1 Value1 Label2 Value2 Label3 Value3 Label4 Value4 blank

Don’t forget the blank at the begining and at the end

Maximum length : 64 bytes     

## Format of message  received by the Jeelink :

###### ASCII-data 

<u>Raw</u>

'OK 2 32 80 65 80 80 32 48 48 51 56 48 32 72 67 72 67 32 48 51 50 49 56 50 32 72 67 72 80 32 48 50 57 57 48 53 32 66 97 116 116 32 48 32 80 114 111 100 32 48 50 51 56 48 55 32 82 65 77 32 56 56 49 0 48 48 0 0'  



<u>After decoding</u>

OK = Acknowledge transmission

2 = Jeenode’s Address  

80 65 80 80 = PAPP  		(Label1)

32 = blank

48 48 51 56 48  = 00380 	(Value1)

32 = blank  

...



<u>After splitting</u>

bytesLineSplitted[0]     Jeenode’s Address  

bytesLineSplitted[1] 	PAPP			(Label1)

bytesLineSplitted[2] 	380			(Value1)

bytesLineSplitted[3] 	...


  
