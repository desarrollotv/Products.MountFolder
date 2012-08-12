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
Tests of MountFolder
"""
__docformat__ = 'restructuredtext'


import os
import sys

from Testing import ZopeTestCase
from Products.Archetypes.tests import ArchetypesTestCase# import ArcheSiteTestCase

import unittest
import Testing
import ZODB
import transaction
from OFS.Application import Application
from OFS.Folder import Folder
import App.config
from Products.ZODBMountPoint.MountedObject import manage_addMounts, getMountPoint
from DBTab.DBTab import DBTab
import Log
Log.LOG_LEVEL = Log.LOG_DEBUG
from Log import *


from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Products.Archetypes.tests import ArchetypesTestCase


try:
    __file__
except NameError:
    __file__ = os.path.abspath(sys.argv[0])

tests = []

class TestDBConfig:
    def __init__(self, fname, mpoints):
        self.fname = fname
        self.mpoints = mpoints

    def getDB(self):
        from ZODB.config import DemoStorage
        from ZODB.Connection import Connection
        from Zope.Startup.datatypes import ZopeDatabase
        self.name = self.fname
        self.base = None
        self.path = os.path.join(os.path.dirname(__file__),  self.fname)
        self.create = None
        self.read_only = None
        self.quota = None
        self.cache_size = 5000
        self.pool_size = 7
        self.version_pool_size = 3
        self.version_cache_size = 100
        self.mount_points = self.mpoints
        self.connection_class = Connection
        self.class_factory = None
        self.storage = DemoStorage(self)
        self.container_class = None
        return ZopeDatabase(self)

    def getSectionName(self):
        return self.name

#tests.append(TestDBConfig)

original_config = None


class MountFolderPloneSiteTestCase(ArchetypesTestCase.ArcheSiteTestCase):
    """ Test case based on a plone site with archetypes including a Mount Folder """

    def afterSetUp(self):
        # login as manager
        user = self.getManagerUser()
        newSecurityManager(None, user)

        # Tools shortcuts
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.undotool = getToolByName(self.portal, 'portal_undo')


    def beforeTearDown(self):
        # logout
        noSecurityManager()

    def _addObjectToMF(self, obj_id='document'):
        """ Utility method for adding an object to the MountFolder """
        self.portal_type = 'Document'  # testing w/ Document
        self.portal.content.invokeFactory(type_name='Document', id=obj_id)

    def test_addContentToMF(self):
        self._addObjectToMF(obj_id='document')
        self.failUnless('document' in self.portal.content.objectIds())

    def test_copyPasteContentInsideMF(self):
        pass

    def test_copyPasteContentFromPloneRootToMF(self):
        pass

    def test_undoContentAddTransactionInsideMF(self):
        self._addObjectToMF(obj_id='document')
        trxs=self.undotool.listUndoableTransactionsFor(self.portal.content)
        tran_id = trxs[0]['id']    # last transaction
        self.undotool.undo(self.portal.content, (tran_id,) )
        document = getattr(self.portal.content, 'document', None)
        self.failUnless(document is None)

#tests.append(MountFolderPloneSiteTestCase)


# Nota:
# Part of this code is 'stolen' from $ZOPE/lib/python/ZODBMountPoint/tests/
class MountFolderTests(ArchetypesTestCase.ArcheSiteTestCase):      #unittest.TestCase):

    def beforeSetUp(self):
        # Change configuration
        Log(LOG_DEBUG, "In _setup()")
        global original_config
        if original_config is None:
            # stow away original config so we can reset it
            original_config = App.config.getConfiguration()

        databases = [TestDBConfig('test_main.fs', ['/']).getDB(),
                     TestDBConfig('test_content.fs', ['/portal/content']).getDB(),
##                     TestDBConfig('test_content2.fs', ['/portal/content2']).getDB(),
                     ]
        mount_points = {}
        mount_factories = {}
        for database in databases:
            points = database.getVirtualMountPaths()
            name = database.config.getSectionName()
            mount_factories[name] = database
            for point in points:
                mount_points[point] = name
        conf = DBTab(mount_factories, mount_points)
        d = App.config.DefaultConfiguration()
        d.dbtab = conf
        App.config.setConfiguration(d)
        self.conf = conf

        # Fire the main DB up
        db = conf.getDatabase('/')
        self.db = db
##        conn = db.open()
##        root = conn.root()
##        root['Application'] = app = Application()
##        self.app = app
##        transaction.commit()  # Get app._p_jar set

##        # XXXXXXX
##        # HERE IS THE PLACE WHERE THE PLONE SITE SHOULD BE CREATED...

##        ArchetypesTestCase.ArcheSiteTestCase._setup(self,)
##        ArchetypesTestCase.ArcheSiteTestCase.afterSetUp(self)
##        transaction.commit()  # Get app._p_jar set
##        print self.app.objectIds()
##        print self.portal.absolute_url()

##        # ...END
##        # XXXXXXX

    def afterSetUp(self,):
        # Now we add the mount point for the content itself
        Log(LOG_DEBUG, "afterSetUp")
        manage_addMounts(self.app, ('/portal/content', ))       #'/portal/content2'))
        transaction.commit()  # Get the mount points ready


    def _clear(self, call_close_hook = 0):
        Log(LOG_DEBUG, "beforeClose", self.app.objectIds())
        transaction.abort()
        transaction.commit()
        ArchetypesTestCase.ArcheSiteTestCase._clear(self, call_close_hook)
        try:            self.app.portal._delObject('content',)
        except:         LogException()
        Log(LOG_DEBUG, "_clear()", self.app.objectIds())
        App.config.setConfiguration(original_config)
        Log(LOG_DEBUG, "_clear()", self.app.objectIds())
        try:        self.app._p_jar.close()
        except:     LogException()
        del self.app
        del self.db
        for db in self.conf.opened.values():
            Log(LOG_DEBUG, "db", db.getName())
            db.close()
        del self.conf

    def testRead(self):
        self.assertEqual(self.app.portal.content.id, 'content')
##        self.assertEqual(self.app.mount2.id, 'mount2')


    def testWrite(self):
        app = self.app
        app.mount1.a1 = '1'
        app.mount2.a2 = '2'
        app.a3 = '3'
        self.assertEqual(app.mount1._p_changed, 1)
        self.assertEqual(app.mount2._p_changed, 1)
        self.assertEqual(app._p_changed, 1)
##        transaction.commit()
        self.assertEqual(app.mount1._p_changed, 0)
        self.assertEqual(app.mount2._p_changed, 0)
        self.assertEqual(app._p_changed, 0)


    def testRaceOnClose(self):
        # There used to be a race condition in
        # ConnectionPatches.close().  The root connection was returned
        # to the pool before the mounted connections were closed.  If
        # another thread pulled the root connection out of the pool
        # before the original thread finished closing mounted
        # connections, when the original thread got control back it
        # closed the mounted connections even though the new thread
        # was using them.

        # Test by patching to watch for a vulnerable moment.

        from ZODB.DB import DB

        def _closeConnection(self, connection):
            self._real_closeConnection(connection)
            mc = connection._mounted_connections
            if mc is not None:
                for c in mc.values():
                    if c._storage is not None:
                        raise AssertionError, "Connection remained partly open"

        DB._real_closeConnection = DB._closeConnection
        DB._closeConnection = _closeConnection
        try:
            conn = self.db.open()
            conn.root()['Application']['mount1']
##            conn.root()['Application']['mount2']
            conn.close()
        finally:
            DB._closeConnection = DB._real_closeConnection
            del DB._real_closeConnection


    def testGetMountPoint(self):
        self.assert_(getMountPoint(self.app) is None)
        self.assert_(getMountPoint(self.app.portal.content) is not None)
        self.assertEqual(getMountPoint(self.app.portal.content)._path, '/portal/content')
##        self.assert_(getMountPoint(self.app.mount2) is not None)
##        self.assertEqual(getMountPoint(self.app.mount2)._path, '/mount2')
##        del self.app.mount2
##        self.app.mount2 = Folder()
##        self.app.mount2.id = 'mount2'
##        self.assert_(getMountPoint(self.app.mount2) is None)
##        transaction.commit()
##        self.assert_(getMountPoint(self.app.mount2) is None)
        del self.app.portal.content
        self.app.portal.content = Folder()
        self.app.portal.content.id = 'content'
        self.assert_(getMountPoint(self.app.portal.content) is None)
##        transaction.commit()
        self.assert_(getMountPoint(self.app.portal.content) is None)

#tests.append(MountFolderTests)







if __name__ == '__main__':
    framework()
else:
    # While framework.py provides its own test_suite()
    # method the testrunner utility does not.
    import unittest
    def test_suite():
        suite = unittest.TestSuite()
        for test in tests:
            suite.addTest(unittest.makeSuite(test))
        return suite
