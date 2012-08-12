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


from common import *
from Products.CMFCore.utils import getToolByName
tests = []

class TestSiteMountFolder(MountFolderTestCase):

    def testAddContentToMf(self, ):
        """
        Add an index_html document
        """
        self.loginAsPortalOwner()
        self.addContent(self.mount_folder, content_id='index_html', type_name='Document')
        self.logout()

    def testCutPaste(self, ):
        """
        Copy paste a content (specially an index_html)
        """
        self.loginAsPortalOwner()
        
        # Create src folder
        folder_id = 'src_folder'
        src_folder = self.addContent(self.mount_folder, content_id=folder_id, type_name='Folder')
        
        # Add document in src folder
        document_id = 'index_html'
        index_html = self.addContent(src_folder, content_id=document_id, type_name='Document')
        
        # Make sure we have _p_jar
        get_transaction().commit(1)
        
        # Create dst folder
        folder_id = 'dst_folder'
        dst_folder = self.addContent(self.mount_folder, content_id=folder_id, type_name='Folder')

        # Cut / Paste
        cb = src_folder.manage_cutObjects(ids=[document_id])
        dst_folder.manage_pasteObjects(cb_copy_data=cb)
        
        # Make sure we have _p_jar
        get_transaction().commit(1)
        
        #new_document = getattr(src_folder, document_id)
        #self.assertEqual(new_document.getId(), document_id)

        self.logout()


tests.append(TestSiteMountFolder)




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
