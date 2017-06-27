## IR remote control
#### This folder contains the files to setup and control the GoPiGo with and Keyes IR remote

------

## What is this Library for?

With this library you can control your `GoPiGo` with a `Keyes Remote Control` by pressing corresponding keys on it.
This means you can make the robot turn to the left, make it go forward, stop, etc. Sky's the limit.

## Example Programs
* `examples/ir_recv_example.py` - run it in order **to test the IR receiver's functionality** - for each pressed key a feedback is printed in the console.
* `examples/gopigo_ir_control_bot.py` - run this script in order **to control your** `GoPiGo` with the `UP`/`DOWN`/`RIGHT`/`UP`/`OK` keys.

## Installation Scripts
* `server/install.sh` - install script for the ir server service - the server is registered as a service in `systemd`.
* `lirc/install.sh` - install script for the lirc dependencies.
* `lirc/ir_install_manually.sh` -  install script for the lirc dependencies - **use this one if you manually reinstall the dependencies**.


## Setup the Hardware
Connect the `IR receiver` to the Serial port on the GoPiGo. This will act as a pass through to the `IR signals` to the `Serial` pins.
* IR receiver (`<= v1.0`) have the IR receiver connected to the `white wire`.
* IR receiver (`v1.1 - 1.2`) have the IR receiver connected to the `yellow wire`.

## Setup the Software

In your `Raspberry Pi`, open up a terminal and enter the following commands:
1. `sudo bash lirc/install.sh`.
2. `sudo bash lirc/setup_older_version.sh` - run this script too only if your version of IR receiver `<= v1.0`.
3. `sudo bash server/install.sh`.

## Enabling / Disabling Service

First, you need to click on `Advanced Communications Options` icon on Desktop.
Select `Enable IR Receiver` and then reboot as required by the app.

**For finer control over the service, here are some commands you can use.**
**All the following commands have to be done on a `Raspberry Pi`.**
**The `ir-server.service` service is responsible for making the IR receiver work or not.**

**For disabling the service type** : `sudo systemctl disable ir-server.service`.
This will cause the IR receiver to not start on the next boot/reboot.

**For stopping the service type** : `sudo systemctl stop ir-server.service`.
This will cause the IR receiver to stop working immediately.
This won't stop the IR receiver from starting again when the `Raspberry Pi` is booted/rebooted, provided the service is enabled.

**For enabling the service type** : `sudo systemctl enable ir-server.service`.
This will cause the IR receiver to start on the next boot/reboot.

**For starting the service type** : `sudo systemctl start ir-server.service`.
This will cause the IR receiver to start working immediately.
This won't make the IR receiver start again when the `Raspberry Pi` is booted/rebooted. For that you need to enable the service.

**For monitoring the status of the service type** : `sudo systemctl status ir-server.service`.
This will print useful information about the status of the `ir-server.service` service.
