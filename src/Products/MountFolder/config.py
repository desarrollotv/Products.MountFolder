# -*- coding: utf-8 -*-
## MountFolder : AT-based Folder that can be used as the root container for a mounted database.
## Copyright (C)2005 Ingeniweb

## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.

## You should have received a copy of the GNU General Public License
## along with this program; see the file COPYING. If not, write to the
## Free Software Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
"""
MountFolder config module
"""
__docformat__ = 'restructuredtext'


import os


PROJECTNAME = "MountFolder"
GLOBALS = globals()
SKINS_DIR = 'skins'

# Check if we have to be in debug mode
import Log
if os.path.isfile(os.path.abspath(os.path.dirname(__file__)) + '/debug.txt'):
    Log.LOG_LEVEL = Log.LOG_DEBUG
else:
    Log.LOG_LEVEL = Log.LOG_NOTICE

from Log import *
Log = Log
Log(LOG_NOTICE, "Starting %s at %d debug level" % (os.path.dirname(__file__), LOG_LEVEL, ))


# Retrieve version
if os.path.isfile(os.path.abspath(os.path.dirname(__file__)) + '/version.txt'):
    __version_file_ = open(os.path.abspath(os.path.dirname(__file__)) + '/version.txt', 'r', )
    version__ = __version_file_.read()[:-1]
else:
    version__ = "(UNKNOWN)"
