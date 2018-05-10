## Installing

You need internet access for the following step(s).

The quickest way for installing the GoPiGo is to enter the following command:
```
curl -kL dexterindustries.com/update_gopigo | bash
```

By default, the GoPiGo package is installed system-wide and [script_tools](https://github.com/DexterInd/script_tools) and [RFR_Tools](https://github.com/DexterInd/RFR_Tools) are updated each time the script is ran.

There's also the classic way of installing the robot where the repository first gets cloned and after that `update_gopigo.sh` is ran the following way:
```
bash update_gopigo.sh
```

An example using options appended to the command can look this way:
```
curl -kL dexterindustries.com/update_gopigo | bash -s --user-local --no-update-aptget --no-dependencies
```

## Command Options

The options that can be appended to this command are:

* `--no-dependencies` - skip installing any dependencies for the GoPiGo. It's supposed to be used on each consecutive update after the initial install has gone through.
* `--no-update-aptget` - to skip using `sudo apt-get update` before installing dependencies. For this to be useful, `--no-dependencies` has to be not used.
* `--bypass-rfrtools` - skips installing RFR_Tools altogether.
* `--bypass-python-rfrtools` - skips installing/updating the python package for  [RFR_Tools](https://github.com/DexterInd/RFR_Tools).
* `--user-local` - install the python package for the GoPiGo in the home directory of the user. This doesn't require any special read/write permissions: the actual command used is (`python setup.py install --force --user`).
* `--env-local` - install the python package for the GoPiGo within the given environment without elevated privileges: the actual command used is (`python setup.py install --force`).
* `--system-wide` - install the python package for the GoPiGo within the sytem-wide environment with `sudo`: the actual command used is (`sudo python setup.py install --force`).

Important to remember is that `--user-local`, `--env-local` and `--system-wide` options are all mutually-exclusive - they cannot be used together.
As a last thing, different versions of it can be pulled by appending a corresponding branch name or tag.

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
