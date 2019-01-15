pyinstaller usini-usbmqtt.py --onefile
rm usini-usbmqtt.spec
cp dist/usini-usbmqtt ../usini-usbmqtt
rm -rf dist
rm -rf build
