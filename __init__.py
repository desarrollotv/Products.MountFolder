__author__  = ''
__docformat__ = 'restructuredtext'

from Products.CMFCore.DirectoryView import registerDirectory

from Products.CMFCore import utils
from Products.CMFCore import CMFCorePermissions

from Products.Archetypes.atapi import process_types, listTypes

from Products.MountFolder.config import PROJECTNAME, SKINS_DIR, GLOBALS
from Products.MountFolder import MountFolder
from Products.MountFolder.MountFolderTool import MountFolderTool

registerDirectory(SKINS_DIR, GLOBALS)

def initialize(context):
    
    # Register classes, constructors and ftis
    content_types, constructors, ftis = process_types(
            listTypes(PROJECTNAME),
            PROJECTNAME)

    utils.ContentInit(
        'Mount Folder',
        content_types      = content_types,
        permission         = CMFCorePermissions.ManagePortal,
        extra_constructors = constructors,
        fti                = ftis,
        ).initialize(context)

    # Initialize tool
    utils.ToolInit(
        '%s Tool' % PROJECTNAME,
        tools=(MountFolderTool,),
        product_name=PROJECTNAME,
        icon='tool.gif'
        ).initialize(context)
