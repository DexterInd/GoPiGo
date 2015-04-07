## Java Library
### This repository contains the Java library for the GoPiGo
#### Installation ####
Before to proceed you should install the Pi4J libraries. The easiest way to install it is using the following command:

```curl -s get.pi4j.com | sudo bash```

If you need more details you can visit the official website: http://pi4j.com/install.html

#### Compile and Execute the test program ####
Once your installation is complete and your local repository is ready then you can compile the GoPiGo libraries and run the test program.
First, enter the Java directory:

```$ cd ./Java/```

The folder structure will be:

```$ config  doc  scripts  src  test```

* **bin** - it's the destination folder for the compiler and it will be created automatically, if not present, by the Bash script.
* **config** - contains the default configuration.
* **doc** - contains the GoPiGo library documentation.
* **scripts** - contains some Bash scripts to compile the library and execute the basic test program.
* **src** - contains the sources of the GoPiGo library.
* **test** - contains some example code/programs.

To compile the library and run the test program you can use the following command:

```$ ./scripts/compile.sh && ./scripts/Test.sh```

By default you will find some logs inside the /var/log/gopigo folder.

In case of any trouble or if you need further information don't hesitate to leave a comment on the official forum: http://www.dexterindustries.com/forum/?forum=gopigo