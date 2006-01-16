__author__  = ''
__docformat__ = 'restructuredtext'

# Python imports
from StringIO import StringIO

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.CMFCorePermissions import ListUndoableChanges

# Archetypes imports
from Products.Archetypes import listTypes
from Products.Archetypes.Extensions.utils import installTypes, install_subskin

# Products imports
from Products.MountFolder.config import GLOBALS, PROJECTNAME
from Products.MountFolder.MountFolderTool import MountFolderTool 

    
def install(self):
    out = StringIO()
    
    # Install types
    typeInfo = listTypes(PROJECTNAME)
    installTypes(self, out,
                 typeInfo,
                 PROJECTNAME)
        
    # Install skin
    install_subskin(self, out, GLOBALS)

    # Install tool
    add_tool = self.manage_addProduct[PROJECTNAME].manage_addTool
    if not self.objectIds(spec=MountFolderTool.meta_type):
        add_tool(MountFolderTool.meta_type)

    atool = getToolByName(self, 'portal_actions')
    atool.addActionProvider(MountFolderTool.id)
    
