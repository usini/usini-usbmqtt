# Arguments parsing
import argparse
import os
import sys
import ConfigParser
import socket

DESCRIPTION = "Connect Serial objects to a mqttServer"
SETTINGS_FILE = "usini-mqttusb.ini"

def get_from_terminal():
    """ Get arguments list

    Returns:
        [args] -- an array of settings
    """

    parser = argparse.ArgumentParser(
        description=DESCRIPTION)
    parser.add_argument("--port", default="",
                        help="Serial port (if no port is set connect to first available port")
    parser.add_argument("--baudrate", default=9600,
                        help="Serial port")
    parser.add_argument("--mqtt", default="127.0.0.1",
                        help="Server url / ip, by default 127.0.0.1")
    parser.add_argument("--mqtt_port", default="1883",
                        help="Mqtt port default: 1883")
    parser.add_argument("--lineending", default="Newline",
                        help="Character to write at end of line Ex: NewLine / No line ending / Carriage return / Both NL & CR")
    parser.add_argument("--username", default="",
                        help="Username"),
    parser.add_argument("--password", default="",
                        help="Password")
    parser.add_argument("--settings_file", default=SETTINGS_FILE,
                        help="Settings location by default: usini-mqttusb.ini")
    parser.add_argument("--topic", default="serial", help="Base Topic name default /serial/")
    parser.add_argument("--debug", default=False, action="store_true",
                        help="Debug Mode")
    parser.add_argument("--ssl", default=False, action="store_true", help="Encrypted connection")
    parser.add_argument("--insecure_cert", default=False, action="store_true", help="Don't check SSL cert")
    args = vars(parser.parse_args())
    if args["debug"]:
        print("Arguments -------------")
        print(args)
    return args

def get_from_file(args_cmd):
    """ Get arguments from a INI Configuration File

    Arguments:
        args {[string]} -- An array previously parsed from command line

    Returns:
        args {[string]} -- Returns arguments
    """
    if os.path.isfile(args_cmd["settings_file"]):
        file = ConfigParser.ConfigParser()
        file.read(args_cmd["settings_file"])
        for name, arg in args_cmd.items():
            try:
                args_cmd[name] = file.get("settings", name)
            except ConfigParser.NoOptionError:
                pass
        if args_cmd["debug"]:
            print("Configuration File -------------")
            print(args_cmd)
    return args_cmd

def get():
    args = get_from_terminal()
    args = get_from_file(args)
    return args