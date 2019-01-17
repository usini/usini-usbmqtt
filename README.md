# usini-usbmqtt
A serial to mqtt gateway in python    
I used pyinstaller to compile it for Linux/Windows/Linux ARM (Raspberry Pi)

Download: https://github.com/usini/usini-usbmqtt/releases

# optional arguments:
```
  -h, --help                    show this help message and exit
  --port PORT                   Serial port default: first available port
  --baudrate BAUDRATE           Baudrate default: 9600
  --mqtt MQTT                   Server url / ip, default: 127.0.0.1
  --mqtt_port MQTT_PORT         Mqtt port default: 1883
  --lineending LINEENDING
                                Character to write at end of line default: NewLine
                                Ex: NewLine / No line ending / Carriage return / Both NL & CR
  --username USERNAME           Username
  --password PASSWORD           Password
  --settings_file SETTINGS_FILE Settings location default: usini-mqttusb.ini
  --topic TOPIC                 Base Topic name default: /serial/
  --debug                       Debug Mode
  --ssl                         Encrypted connection
  --insecure_cert               Don't check SSL certificate
```

# How to use it
When connected to a serial device, usini-usbmqtt generate these topics (with retain)

* /serial/PORT/in : Send a message to serial device
* /serial/PORT/out : Receive a messae from serial device
* /serial/PORT/baudrate : Change baudrate and reconnect
* /serial/PORT/lineending : Change lineending
* /serial/PORT/status : Display current status (offline / online / serialerror)
