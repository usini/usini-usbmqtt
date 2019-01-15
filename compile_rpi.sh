pyinstaller usini-usbmqtt.py --onefile
rm usini-usbmqtt.spec
cp dist/usini-usbmqtt ../usini-usbmqtt_rpi
rm -rf dist
rm -rf build
