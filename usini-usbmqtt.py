'''
    usini-usbmqtt : Connect a serial port to mqtt
    Author : Remi Sarrailh
    Email : remi@madnerd.org
    License : MIT
'''

import sys
import serial
import time
from modules import Settings
import paho.mqtt.client as mqtt

global client, serial_ok, port, topic, args, device

"""Convert line Ending settings to line ending
Returns:
    String -- lineending
"""
def convert_lineending(lineending_arg):
    lineending = "\n" # Default to newLine
    if lineending_arg == "Both NL & CR":
        print("Both NL & CR set")
	lineending = "\n\r"
    if lineending_arg == "Carriage return":
        lineending = "\r"
	print("Carriage return set")
    if lineending_arg == "Newline":
        lineending = "\n"
	print("New Line set")
    if lineending_arg == "No line ending":
        lineending = ""
	print("No line ending set")
    lineending = lineending.encode()
    return lineending

""" When the serial object is connected
"""
def serial_connect(baudrate):
    global device, args, serial_ok

    if serial_ok == True:
        print "Closing previous device"
        device.close()
        serial_ok = False

    # Serial Connection
    try:
        device = serial.Serial(args["port"], baudrate, timeout=1)
        serial_ok = True
        print("Open " + str(args["port"]) + " baudrate:" + str(baudrate) + " lineending:" + args["lineending"])
    except Exception as e:
        print("!! Serial failure !! : " + str(e))
        time.sleep(5)
        serial_ok = False
        sys.exit(1)

""" When a serial message is received
"""
def on_serial_message():
        global device, serial_ok, args
        if serial_ok:
                try:
                    data = b''
                    data = device.readline()
                    if data is not b'':
                        data = data.decode(encoding='utf-8', errors="replace")
                        client.publish(args["topic-out"],format(data.encode('utf-8')) , retain=True)
                        print(args["topic-out"] + " -- " + data)

                except Exception as e:
                    print("[" + args["topic"] + "] --> " + " ERROR " + str(e))
                    serial_ok = False
                    device.close()
                    sys.exit(1)

""" When the serial object is connected to a mqtt server
"""

def on_mqtt_connect(client, userdata, flags, rc):
    global reconnection_need
    if(rc == 0):
        reconnection_need = False
        print("Connected to " + args["mqtt"] + ":" + str(args["mqtt_port"]))
        print("--------------------")

        print("TX - " + args["topic-in"])
        print("RX - " + args["topic-out"])

        client.publish(args["topic-lineending"], args["lineending"], retain=True)
        client.publish(args["topic-baudrate"], args["baudrate"], retain=True)

        client.publish(args["topic-status"], "online", retain=True)

        client.subscribe(args["topic-in"])
        client.subscribe(args["topic-out"])
        client.subscribe(args["topic-baudrate"])
        client.subscribe(args["topic-lineending"])
    else:
        if(rc == 5):
            print("Connection failed: Wrong username or password")
        else:
            print("Connection failed : " + str(rc))
        sys.exit(1)

""" When a mqtt message is received
"""

def on_mqtt_message(client, userdata, message):
    global devices,args

    # If message is sent to serial object
    if message.topic == args["topic-in"]:
        print(message.topic + " -- " + message.payload)
        try:
            data = message.payload.encode(encoding="utf-8", errors="replace")
            device.write(data + args["lineending_encode"])
        except UnicodeDecodeError:
            print("Decoding error, ignore...")
        except Exception as e:
            print("[" + args["topic"] + "] --> " + " SERIAL WRITE ERROR " + str(e))
            device.close()
            serial_ok = False

    # If lineending is changed
    if message.topic == args["topic-lineending"]:
        print(message.topic + " -- " + message.payload)
        args["lineending_encode"] = convert_lineending(message.payload)

    # If baudrate is changed
    if message.topic == args["topic-baudrate"]:
        print(message.topic + " -- " + message.payload)
        args["baudrate"] = message.payload
        serial_connect(message.payload)

def on_mqtt_disconnect(client, userdata, rc):
    global reconnection_need
    print "Unexpected MQTT disconnection. Attempting to reconnect."
    reconnection_need = True


print("usini-usbmqtt ----(Beta v0.1)---------")
print("https://github.com/usini/usini-usbmqtt")
print("--------------------------------------")
args = Settings.get() #Get settings from command line or settings file (default usini-usbmqtt.ini)
serial_ok = False
reconnection_need = False
#If no port is provided search for first pid
if(args["port"] == ""):
    from serial.tools import list_ports
    for serial_device in list_ports.comports():
        if(serial_device.pid != None):
            args["port"] = serial_device.device

#args["lineending_encode"] = convert_lineending(args["lineending"]);

args["topic"] = "/serial/"

#Workaround for linux to avoid bogus topics
if args["port"].startswith("/"):
    temp_array = args["port"].split("/")
    args["topic"] = args["topic"] + temp_array[len(temp_array) -1]
else :
    args["topic"] = args["topic"] + args["port"]

args["topic-in"] = args["topic"] + "/in"
args["topic-out"] = args["topic"] + "/out"
args["topic-baudrate"] = args["topic"] + "/baudrate"
args["topic-lineending"] = args["topic"] + "/lineending"
args["topic-status"] = args["topic"] + "/status"

args["baudrate"] = int(args["baudrate"])
args["mqtt_port"] = int(args["mqtt_port"])

client = mqtt.Client()
client.on_connect = on_mqtt_connect
client.on_message = on_mqtt_message
client.on_disconnect = on_mqtt_disconnect
client.will_set(args["topic-status"],"offline", retain=True)


if(args["ssl"]):
    client.tls_set()
    client.tls_insecure_set(args["insecure_cert"])

if(args["username"] != ""):
    client.username_pw_set(username=args["username"], password=args["password"])
try:
    client.connect(args["mqtt"], args["mqtt_port"], 60)
except Exception as e:
    print("No MQTT Server Founded !! : " + str(e))
    time.sleep(5)
    sys.exit(1)

run = True
while run:
    on_serial_message()
    client.loop()
    if reconnection_need:
        try:
            client.reconnect()
        except:
            print("...")
