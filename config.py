# -*- coding: latin-1 -*-
__author__  = ''
__docformat__ = 'restructuredtext'

import os


PROJECTNAME = "MountFolder"
GLOBALS = globals()
SKINS_DIR = 'skins'


## using special plone 2 stuff? (copied from ATCT's config.py)
try:
    from Products.CMFPlone.PloneFolder import ReplaceableWrapper
except ImportError:
    HAS_PLONE2 = False
else:
    HAS_PLONE2 = True
    del ReplaceableWrapper
        
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
