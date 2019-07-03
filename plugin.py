# Jeelink Python Plugin 
#
# Author: Moustache13 & Cyrilsansfeunilieu
#
"""
<plugin key="Jeelink" name="Jeelink" author="moustache13" version="0.1">
    <description>
        <h2>Plugin Jeelink USB</h2><br/>
        <h3>Features</h3>
        <ul style="list-style-type:square">
            <li>Connection with Jeelink</li>
            <li>Read Messages from Jeenodes</li>
        </ul>
        <h3>Devices</h3>
        <ul style="list-style-type:square">
            <li>Devices defined by user in the Jeenode's sketche </li>
        </ul>
        <h3>Configuration</h3>
    </description>
    <params>
        <param field="SerialPort" label="Serial Port" width="150px" required="true" default="/dev/ttyRAVEn"/>
        <param field="Mode6" label="Debug" width="100px">
            <options>
                <option label="True" value="Debug"/>
                <option label="False" value="Normal"  default="true" />
                <option label="Logging" value="File"/>
            </options>
        </param>
    </params>
</plugin>
"""
import Domoticz
import re

SerialConn = None

class BasePlugin:
    enabled = False
    def __init__(self):
        #self.var = 123
        return

    def onStart(self):
        global SerialConn
        Domoticz.Log("onStart called")
        if Parameters["Mode6"] != "Normal":
           Domoticz.Debugging(1)
        if Parameters["Mode6"] == "Debug":
           Domoticz.Debug("debug mode enable")

        if (len(Devices) == 0):
           Domoticz.Device(Name="PAPP", Unit=1, TypeName="Usage").Create()
           Domoticz.Log("Devices created.")
#       add new Devices one by one hier and restart ...
#       Example
#          if (len(Devices) == 1):
#          Domoticz.Device(Name="Teleinfo EDF", Unit=2, Type=250, Subtype=1, Switchtype=0).Create()

        Domoticz.Log("Plugin has " + str(len(Devices)) + " devices associated with it.")

        for Device in Devices:
            Devices[Device].Update(nValue=Devices[Device].nValue, sValue=Devices[Device].sValue, TimedOut=1)
        SerialConn = Domoticz.Connection(Name="Jeelink", Transport="Serial", Protocol="Line", Address=Parameters["SerialPort"], Baud=57600)
        SerialConn.Connect()
        DumpConfigToLog()
 

    def onStop(self):
        Domoticz.Log("onStop called")

    def onConnect(self, Connection, Status, Description):
        global SerialConn
        Domoticz.Log("onConnect called")
        if (Status == 0):
           Domoticz.Log("Connected successfully to: "+Parameters["SerialPort"])
           SerialConn = Connection
        else:
           Domoticz.Log("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"])
           Domoticz.Debug("Failed to connect ("+str(Status)+") to: "+Parameters["SerialPort"]+" with error: "+Description)

    def onMessage(self, Connection, Data):
        Domoticz.Debug("onMessage called")
        if (len(Data) == 0):
           Domoticz.Log("no data message")
           return
        Domoticz.Debug("data len : " + str(len(Data)) + " ---- data : " + Data.decode())
        for line in Data.split(b"\n"):
           Domoticz.Debug("line" + str(line))
           Data.replace(b'\0',b'')
           lineSplitted = list(filter(None,line.strip().split(b' ')))
           Domoticz.Debug("lineSplitted[0]" + str(lineSplitted[0]))
           try:
            if (lineSplitted[0] == b'OK'):  # read only message starting with "OK" 
                bytesLine = bytearray(map(lambda x: int(x),lineSplitted[1:]))
           except ValueError as ve:
              Domoticz.Error(str(ve))
              continue
           if (lineSplitted[0] == b'OK'):  
            Domoticz.Debug("line converted : " + str(bytesLine))
            bytesLineSplitted = bytesLine.split(b" ")
            # clean end of message 
            bytesLineSplitted[12] = bytesLineSplitted[12].hex() # convert  hex to str
            del bytesLineSplitted[12]
            bytesLineSplitted[11] = bytesLineSplitted[11].hex() # convert  hex to str
            del bytesLineSplitted[11]
            Domoticz.Debug("line INT splitted : " + str(bytesLineSplitted))

            Node_id = str(int(bytesLineSplitted[0].hex())) # convert jeenode address hex to str
            Domoticz.Debug("Jeenode Address : " + Node_id)
            iPAPP = str(int(bytesLineSplitted[2]))
            Domoticz.Debug("isValue : " + iPAPP)

            # update devices sValue dashboard from selected Node_id
            if (Node_id == "2"):
                   Devices[1].Update(nValue=0, sValue=iPAPP, TimedOut=0)
		   # add update sValue hier

            else:
               Domoticz.Debug("Node_id unknown", Node_id) 

    def onCommand(self, Unit, Command, Level, Hue):
        Domoticz.Log("onCommand called for Unit " + str(Unit) + ": Parameter '" + str(Command) + "', Level: " + str(Level))

    def onNotification(self, Name, Subject, Text, Status, Priority, Sound, ImageFile):
        Domoticz.Log("Notification: " + Name + "," + Subject + "," + Text + "," + Status + "," + str(Priority) + "," + Sound + "," + ImageFile)

    def onDisconnect(self, Connection):
        Domoticz.Log("onDisconnect called")

    def onHeartbeat(self):
        #Domoticz.Log("onHeartbeat called")
        if not SerialConn.Connected():
           Domoticz.Error("Lost connection with device")
           SerialConn.Connect()

global _plugin
_plugin = BasePlugin()

def onStart():
    global _plugin
    _plugin.onStart()

def onStop():
    global _plugin
    _plugin.onStop()

def onConnect(Connection, Status, Description):
    global _plugin
    _plugin.onConnect(Connection, Status, Description)

def onMessage(Connection, Data):
    global _plugin
    _plugin.onMessage(Connection, Data)

def onCommand(Unit, Command, Level, Hue):
    global _plugin
    _plugin.onCommand(Unit, Command, Level, Hue)

def onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile):
    global _plugin
    _plugin.onNotification(Name, Subject, Text, Status, Priority, Sound, ImageFile)

def onDisconnect(Connection):
    global _plugin
    _plugin.onDisconnect(Connection)

def onHeartbeat():
    global _plugin
    _plugin.onHeartbeat()

    # Generic helper functions
def DumpConfigToLog():
    for x in Parameters:
        if Parameters[x] != "":
            Domoticz.Debug( "'" + x + "':'" + str(Parameters[x]) + "'")
    Domoticz.Debug("Device count: " + str(len(Devices)))
    for x in Devices:
        Domoticz.Debug("Device:           " + str(x) + " - " + str(Devices[x]))
        Domoticz.Debug("Device ID:       '" + str(Devices[x].ID) + "'")
        Domoticz.Debug("Device Name:     '" + Devices[x].Name + "'")
        Domoticz.Debug("Device nValue:    " + str(Devices[x].nValue))
        Domoticz.Debug("Device sValue:   '" + Devices[x].sValue + "'")
        Domoticz.Debug("Device LastLevel: " + str(Devices[x].LastLevel))
    return
