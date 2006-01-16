"""
MountFolder base test

$Id$
"""

__author__ = ''
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