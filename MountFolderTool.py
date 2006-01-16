"""
$Id$
"""

__author__  = ''
__docformat__ = 'restructuredtext'

# Zope imports
from Globals import InitializeClass
from AccessControl import ClassSecurityInfo
from OFS.SimpleItem import SimpleItem
from OFS.PropertyManager import PropertyManager

# CMF imports
from Products.CMFCore.utils import UniqueObject, getToolByName
from Products.CMFCore.ActionProviderBase import ActionProviderBase
from Products.CMFCore import CMFCorePermissions
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
                              , permissions=(CMFCorePermissions.ListUndoableChanges, )
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
                              , permissions=(CMFCorePermissions.ListUndoableChanges, )
                              , category='user'
                              , condition=Expression(text="python:member and not portal.portal_mountfolder.getMountFolder(object)")
                              , visible=1
                              )
          )
          

    security = ClassSecurityInfo()
                

    security.declareProtected(CMFCorePermissions.View, 'getMountFolder')
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
    
    security.declareProtected(CMFCorePermissions.View, 'getMountFolderUrl')
    def getMountFolderUrl(self, object):
        """
        Get the containing MountFolder's URL.
        """
        mf = self.getMountFolder(object, mfolders_container=None)
        return mf.absolute_url()

InitializeClass(MountFolderTool)
