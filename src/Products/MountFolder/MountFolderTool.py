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
MountFolder helper tool
"""
__docformat__ = 'restructuredtext'


# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import permissions
from Products.CMFCore.ActionInformation import ActionInformation
from Products.CMFCore.Expression import Expression


class MountFolderTool(PropertyManager, UniqueObject, SimpleItem, ActionProviderBase):
    """Helper tool for MountFolder"""

    plone_tool = True
    id = 'portal_mountfolder'
    title = "Provides actions and logic used by MountFolder instances"
    meta_type = "MountFolderTool"
    
    _properties=(
        {'id':'title', 'type': 'string', 'mode':'w'},)
                    
    manage_options = (ActionProviderBase.manage_options + \
                      PropertyManager.manage_options + \
                      SimpleItem.manage_options)

    _actions = ( ActionInformation( id='undo'
                              , title='Undo'
                              , description=''
                              , action=Expression(
                                 text="python:portal.portal_mountfolder.getMountFolderUrl(object) + '/mf_undo_form'")
                              , permissions=(permissions.ListUndoableChanges, )
                              , category='user'
                              , condition=Expression(text="python:member and portal.portal_mountfolder.getMountFolder(object)")
                              , visible=1
                              )
           ,
           ActionInformation( id='undo'
                              , title='Undo'
                              , description=''
                              , action=Expression(
                                 text='string:$portal_url/undo_form')
                              , permissions=(permissions.ListUndoableChanges, )
                              , category='user'
                              , condition=Expression(text="python:member and not portal.portal_mountfolder.getMountFolder(object)")
                              , visible=1
                              )
          )
          

    security = ClassSecurityInfo()
                

    security.declareProtected(permissions.View, 'getMountFolder')
    def getMountFolder(self, object, mfolders_container=None):
        """
        Get the containing MountFolder of an object,
        assuming we can have several mountfolders inside a common container.
        If not specified, this common container is the portal object.
        """
        portal = getToolByName(object, 'portal_url').getPortalObject()
        mfolders = []
        if not mfolders_container:
            mfolders = portal.objectValues(['MountFolder'])
        object_path = object.getPhysicalPath()
        
        for folder in mfolders:
            if folder.getId() in object_path:
                return folder
    
    security.declareProtected(permissions.View, 'getMountFolderUrl')
    def getMountFolderUrl(self, object):
        """
        Get the containing MountFolder's URL.
        """
        mf = self.getMountFolder(object, mfolders_container=None)
        return mf.absolute_url()

InitializeClass(MountFolderTool)
