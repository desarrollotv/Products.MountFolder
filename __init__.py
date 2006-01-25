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
MountFolder init module
"""
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
