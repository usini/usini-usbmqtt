pyinstaller usini-usbmqtt.py --onefile --icon usini-usbmqtt.ico
del usini-usbmqtt.spec
copy dist\usini-usbmqtt.exe ..\
rmdir /s /q dist
rmdir /s /q build
