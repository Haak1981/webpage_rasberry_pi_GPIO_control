This project sets up a small webserver which hosts a simple website with a button which in turn controls (activates/deactivates) a Raspberry Pi GPIO pin. It also checks the status of a sensor to see if this is OFF or ON.

it uses Uvicorn as the webserver.


tip:
set port forwarding on local modem. Raspberry pi ip-address forward port 80. Maybe necessary to first make a static ip-address for pi.

update A-record at webhost to forward to raspberry pi public ip-address
