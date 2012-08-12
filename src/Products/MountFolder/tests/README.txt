This is a description of the testcase we should run.



What you have to do to test this is the following:

     * Update your Zope configuration to store 'content' mount point:
     <zodb_db content>
         <filestorage>
               path $INSTANCE/var/DataContent.fs
         </filestorage>
         mount-point /plonesite/content
         container-class Products.MountFolder.MountFolder.MountFolder
     </zodb_db>

     * Create Plone Site
     * Create a MountFolder called 'content' inside
     * Create content inside, then UNDO it to check if transactions work

