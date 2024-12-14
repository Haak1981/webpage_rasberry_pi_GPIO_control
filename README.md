This project sets up a small webserver which host a simple website with a button which in turn control (activates/deactivates) a Raspberry Pi GPIO. It also checks the status of a sensor on to see if this is OFF or ON

it uses Uvicorn as the webserver.


tip:
set port forwarding on local modem. Raspberry pi ip-address forward port 80. Maybe necessary to first make a static ip-address for pi

update A-record at webhost to forward to raspberry pi public ip-address
