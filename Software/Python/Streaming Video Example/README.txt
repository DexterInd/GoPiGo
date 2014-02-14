There are two parts to this example:

Streaming the Video:
	- Attach the camera to the GOPIGO.
	- Follow these instructions for setup of the server and camera:  http://www.miguelmota.com/blog/raspberry-pi-camera-board-video-streaming/
	- chmod 777 both scripts (.sh) files.

Setting up the Robot:
	- Flash the Arduino Firmware (remember to use CTRL+SHIFT+U!)

Running the System:
	- Run the "start_streaming.sh" script under sudo.
	- This will start the python program as well.
	- Start VLC Media Player.
	- If you're on the same network, open the network stream "http://raspberrypi.local:9000/?action=stream"