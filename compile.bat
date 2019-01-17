pyinstaller usini-usbmqtt.py --onefile --icon usini-usbmqtt.ico
del usini-usbmqtt.spec
move dist\usini-usbmqtt.exe ..\usini-usbmqtt_win.exe
rmdir /s /q dist
rmdir /s /q build
