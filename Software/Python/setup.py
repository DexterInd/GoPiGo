#!/usr/bin/env python
#
'''
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
'''

import setuptools

# Get version from pkg index
from gopigo import __version__
from gopigo import __author__
from gopigo import __maintainer__
from gopigo import __url__
from gopigo import __email__
from gopigo import __doc__
from gopigo import __shortdesc__
from gopigo import __name__ as __packagename__

desc = __shortdesc__
long_desc = __doc__

requires = []

setuptools.setup(name="GoPiGo",
    version=__version__,
    description=desc,
    long_description=long_desc,
    author=__author__,
    #author_email=__email__,
    url=__url__,
    packages=setuptools.find_packages(),
    install_requires=requires,
)
