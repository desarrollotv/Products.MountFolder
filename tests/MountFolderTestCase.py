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
MountFolder base test
"""
__docformat__ = 'restructuredtext'


# Python imports
import time
import os

# Zope imports
from Testing import ZopeTestCase
from AccessControl.SecurityManagement import newSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from Acquisition import aq_base
import App.config
from Products.ZODBMountPoint.MountedObject import manage_addMounts, getMountPoint
from DBTab.DBTab import DBTab

# CMF imports
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# Products imports
from Products.MountFolder.Extensions.Install import install as installMountFolder

# Plone imports
from Products.CMFPlone.tests import PloneTestCase

# Portal users
portal_name = PloneTestCase.portal_name
portal_owner = PloneTestCase.portal_owner
portal_member = 'portal_member'
portal_member2 = 'portal_member2'

# ZODB Mount point
mountfolder_path = '/portal/content'

try:
    __file__
except NameError:
    __file__ = os.path.abspath(sys.argv[0])

class TestDBConfig:
    def __init__(self, fname, mpoints, container_class=None):
        self.fname = fname
        self.mpoints = mpoints
        self.container_class = container_class
    
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
        self.container_class = self.container_class
        return ZopeDatabase(self)

    def getSectionName(self):
        return self.name

original_config = None


class MountFolderTestCase(PloneTestCase.PloneTestCase):
    """ MountFolder test case based on a plone site"""
    
    def afterSetUp(self):
        # Tools shortcuts
        self.ttool = getToolByName(self.portal, 'portal_types')
        self.wftool = getToolByName(self.portal, 'portal_workflow')
        self.mbtool = getToolByName(self.portal, 'portal_membership')
        self.mftool = getToolByName(self.portal, 'portal_mountfolder')
        self.member_folder = self.mbtool.getHomeFolder(portal_member)
        # Add role reviewer to portal_member in member_folder
        self.member_folder.manage_addLocalRoles(portal_member, roles = ['Reviewer',])
        # Mount folder shortcut
        self.mount_folder = getattr(self.portal, 'content')
        
    def createMountFolder(self, container, content_id = 'mf', wf_action=None):
        """
        Create and return a MountFolder
        """
        # make sure we can add an object of this type to the container
        self.ttool.MountFolder.manage_changeProperties(global_allow=1)

        container.invokeFactory(type_name='MountFolder', id=content_id)
        self.failUnless(content_id in container.objectIds())
        self.mf = getattr(container, content_id)
        self.assertEqual(self.mf.title, '')
        self.assertEqual(self.mf.getId(), content_id)

        if wf_action is not None:
            self.wftool.doActionFor(self.mf, wf_action)
        return self.mf

    def addContent(self, container, content_id='index_html', type_name='Document'):
        container.invokeFactory(type_name=type_name, id=content_id)
        content = getattr(container, content_id)
        self.assertEqual(content.title, '')
        self.assertEqual(content.getId(), content_id)

        return content

    def beforeTearDown(self):
        # logout
        noSecurityManager()

    def loginAsPortalMember(self):
        '''Use if you need to manipulate an object as member.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member).__of__(uf)
        newSecurityManager(None, user)

    def loginAsPortalMember2(self):
        '''Use if you need to manipulate an object as member.'''
        uf = self.portal.acl_users
        user = uf.getUserById(portal_member2).__of__(uf)
        newSecurityManager(None, user)

    def loginAsPortalOwner(self):
        '''Use if you need to manipulate an object as portal owner.'''
        uf = self.app.acl_users
        user = uf.getUserById(portal_owner).__of__(uf)
        newSecurityManager(None, user)

def setupMountFolder(app, quiet=0):
    get_transaction().begin()
    _start = time.time()
    portal = app.portal

    if not quiet: ZopeTestCase._print('Installing MountFolder ... ')

    # login as manager
    user = app.acl_users.getUserById(portal_owner).__of__(app.acl_users)
    newSecurityManager(None, user)
    
    # add MountFolder
    if hasattr(aq_base(portal), 'portal_mountfolder'):
        ZopeTestCase._print('MountFolder already installed ... ')
    else:
        installMountFolder(portal)

    # Initialized MountPoint
    manage_addMounts(app, (mountfolder_path,))
    get_transaction().commit()

    # Create portal member
    portal.portal_registration.addMember(portal_member, 'azerty', ['Member'])
    portal.portal_registration.addMember(portal_member2, 'azerty', ['Member'])

    # Log out
    noSecurityManager()
    get_transaction().commit()
    if not quiet: ZopeTestCase._print('done (%.3fs)\n' % (time.time()-_start,))
    
def setupMountPoint():
    import App.config
    config = App.config.getConfiguration()
    databases = [TestDBConfig('test_main.fs', ['/']).getDB(),
                 TestDBConfig('test_mount1.fs', [mountfolder_path], 'Products.MountFolder.MountFolder.MountFolder').getDB(),
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

setupMountPoint()
app = ZopeTestCase.app()
setupMountFolder(app)
ZopeTestCase.close(app)
