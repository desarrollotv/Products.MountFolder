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
MountFolder install module
"""
__docformat__ = 'restructuredtext'


# Python imports
from StringIO import StringIO

# CMF imports
from Products.CMFCore.utils import getToolByName
from Products.CMFCore.permissions import ListUndoableChanges

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
    
