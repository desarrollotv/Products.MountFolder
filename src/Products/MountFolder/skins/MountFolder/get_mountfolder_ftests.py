## Script (Python) "get_mountfolder_ftests"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=
##

# For this test suite to work, add the following to your zope.conf:
#<zodb_db content>
#    <filestorage>
#      path $INSTANCE/var/Content.fs
#    </filestorage>
#    mount-point /plonesite/content
#    container-class Products.MountFolder.MountFolder.MountFolder
#</zodb_db>

selenium = context.portal_selenium

selenium.addUser(id = 'sampleadmin',fullname='Sample Admin',roles=['Member', 'Manager',])
selenium.addUser(id = 'samplemember',fullname='Sample Member',roles=['Member',])

suite = selenium.getSuite()

test_logout = suite.TestLogout()
test_admin_login  = suite.TestLoginPortlet('sampleadmin')
test_switch_language = suite.TestSwitchToLanguage()

mount_id = "content"

test_add_mount_point = t = suite.getTest()
t.open("/manage_addProduct/ZODBMountPoint/addMountsForm")
t.click("create_mount_points")
t.clickAndWait("submit")
t.open("/%s/manage_main" % mount_id)
t.verifyTextPresent("MountFolder at")

test_publish_mount_point = t = suite.getTest()
t.open("/%s" % mount_id)
t.open("/%s/content_status_modify?workflow_action=publish" % mount_id)
#t.verifyTextPresent("State: published")

def test_add_numbered_content(doc_num):
    t = suite.getTest()
    document_id = "doc%s" % str(doc_num)
    document_title = "Test Document %s" % doc_num
    t.open("/%s/createObject?type_name=Document" % mount_id ),
    t.type("id", document_id),
    t.type("title", document_title),
    t.type("description","This is a test document"),
    t.type("text","This is the body text of the test document"),
    t.clickAndWait("form_submit"),
    t.verifyTextPresent("Your changes have been saved."),
    return t

test_undo = t = suite.getTest()
t.open("/%s/mf_undo_form" % mount_id )

test_delete_content = t = suite.getTest()
t.open("/%s/folder_contents" % mount_id)
t.open("/%s/folder_delete?ids:list=%s" % (mount_id,'doc1'))
t.verifyTextPresent("has been deleted.")

test_delete_mount_point = t = suite.getTest()
t.open("/folder_delete?ids:list=%s" % mount_id)
t.verifyTextPresent("%s has been deleted." % mount_id)

suite.addTests("Add MountFolder and Populate it with content",
          'Login as Sample Admin',
          test_logout,
          test_admin_login,
          test_switch_language,
          'Add Mount Point',
          test_add_mount_point,
          'Publish Mount Point',
          test_publish_mount_point,
          'Add document 1',
          test_add_numbered_content(1),
          'Add document 2',
          test_add_numbered_content(2),
          'Add document 3',
          test_add_numbered_content(3),
          'Add document 4',
          test_add_numbered_content(4),
         )

suite.addTests("Undo",
          'Undo Add document',
          test_undo
         )

suite.addTests("Delete MountFolder",
          'Login as Sample Admin',
          test_logout,
          test_admin_login,
          test_switch_language,
          'Add MountFolder',
          test_add_mount_point,
          'Add a document',
          test_add_numbered_content(1),
          'Delete the document added (inside the MF)',
          test_delete_content,
          'Delete MountFolder',
          test_delete_mount_point
         )

# Create document, e.g. ATDocument
# Delete document
# Error in log: Try to unreference dated object in /content
 
             
return suite
