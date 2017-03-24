#GoPiGo in C

This repository contains source code, firmware and design materials for the GoPiGo in the C Language.

#####To Compile:  gcc gopigo.c [your_file_name.c] -o gopigo -Wall
#####To run: ./gopigo

**Notes:**
- The compile command uses the basic commands from gopigo.c library 
- The output exectuable is the one followed by the -o argument, which is gopigo here (You can change it to something else if yuo want)
- the -Wall argument enable's all compiler warnings and is necessary for compiling the GoPiGo C example. Read more about it here: http://www.rapidtables.com/code/linux/gcc/gcc-wall.htm 

## Dedicated library
If you want to use the library in a couple of different projects, it is recommended to install it globally. This also provides the information needed for pkg-config and CMake to automatically locate the library for more complex projects and build systems.
#### Building with CMake
First, we create a dedicated build directory:
```
mkdir build
cd build
```
Now we can either create a Debian package
```
cmake ..
make package
```
and install it within Raspbian
```
sudo dpkg -i libgopigo-<version>-Linux-dev.deb
```
where `<version>` might be something like 1.6 (e.g., libgopigo-1.6-Linux-dev.deb).

Or, if you run the GoPiGo with any other non-Debian like Linux, it can be installed manually to an arbitrary folder:
```
cmake -DCMAKE_INSTALL_PREFIX=/usr/local/ ..
sudo make install
```

#### Build example programm and link against libgopigo
To use the install library directly with gcc, you need to link against it (```-lgopigo```) at compile time:
```
gcc basic_test_all.c -o gopigo -lgopigo -Wall
```
This way, the our new executable gopigo will use the previously install library *libgopigo.so.1.6*.
Append *-static* to the above line, if you want to distribute the executable without the dependency on the gopigo library.

For using the library in a cmake project, change your _CMakeLists.txt_ to locate the package via:
```
find_package(gopigo REQUIRED)
```
and link the library:
```
target_link_libraries(your_executable ${gopigo_LIBRARIES})
```

![ GoPiGo ](https://raw.githubusercontent.com/DexterInd/GoPiGo/master/GoPiGo_Front_Facing_Camera300.jpg)

#See Also

- [Dexter Industries] (http://www.dexterindustries.com/GoPiGo)
- [Kickstarter Campaign] (http://kck.st/Q6vVOP)
- [Raspberry Pi] (http://www.raspberrypi.org/)

## License
GoPiGo for the Raspberry Pi: an open source robotics platform for the Raspberry Pi.
Copyright (C) 2017  Dexter Industries

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
