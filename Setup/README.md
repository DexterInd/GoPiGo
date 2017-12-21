## Installing

This is the install script for the GoPiGo which installs all the packages and libraries need for running the GoPiGo.

For installing the GoPiGo you should only enter one of the 2 following command(s):
```
# for installing the python packages with root permissions (except anything else which will ran as root) run this
sudo sh -c "curl -kL dexterindustries.com/update_tools | bash"

# for installing the python packages with user permissions (except anything else which will ran as root) run this
curl -kL dexterindustries.com/update_tools | bash
```

Or if you want the classic way, you can clone the repository, change directory to this folder and then enter the following command:
```
# for root privileges
sudo bash install.sh

# for user privileges
```

Make sure that you are connected to the internet before starting.

## License
GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2015  Dexter Industries

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/gpl-3.0.txt>.
