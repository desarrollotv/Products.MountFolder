Mount Folder for Plone
======================

  This product provides an AT-based Folder that can be used as the root container for a mounted database.

  This was needed as a separate folder class, since the standard ATFolder does not (at the time of writing) support the mount operation due to its dependency on the reference system (among other things). We were facing a traversal/acquisition bug triggered by the call to the 'reference_catalog' object from ATFolder's (or BaseFolder's) 'manage_afterAdd' method.

Dependencies
============

Required Products
------------------

* Plone 2.0
* Archetypes >= 1.3.2

Installation
============

Basic Zope setup details
------------------------

1- Copy to the usual 'Products' directory.

2- Update your zope.conf file accordingly by adding the zodb_db configuration ::

  <zodb_db content>
    <filestorage>
      path $INSTANCE/var/DataContent.fs
    </filestorage>
    mount-point /myplonesite/content
    container-class Products.MountFolder.MountFolder.MountFolder
  </zodb_db>

3- Restart Zope.

4- Go to your Plone site and "QuickInstall" the product.

5- Via the ZMI, add a 'ZODB Mount Point' object within the Plone site. Remember to check the box to add new folders.

ZEO setup details
-----------------

1- Install zeo and zope clients. (For more info, see the excellent http://plone.org/documentation/tutorial/robust-installation/installing-zope/)

2- In your zeo.conf, define a new filestorage as follows (where "content" is the name of the storage, with the path $INSTANCE/var/DataContent.fs) ::

  <filestorage content>
    path $INSTANCE/var/DataContent.fs
  </filestorage>

3- In each client's zope.conf, add the mount point's configuration as follows (where "content" is the name of the storage) ::

  <zodb_db content>
    mount-point /myplonesite/content
    container-class Products.MountFolder.MountFolder.MountFolder
    <zeoclient>
      server localhost:4200
      storage content
      name zeostoragecontent
      var $INSTANCE/var
      cache-size 20MB
    </zeoclient>
  </zodb_db>

4- For each client, via the ZMI, proceed as usual to add a 'ZODB Mount Point' object within the Plone site.

TODO
====

Bugs / Issues
-------------

* Impossible to do a _cut and paste_ operation between the MountFolder and another space of the Plone site.

  (Error Type: InvalidObjectReference - Error Value: Attempt to store an object from a foreign database connection.)

 o the main part of the ZODB (Data.fs). Have to test this with normal Folder-based mounts to see if its normal from ZODB P.O.V.

* Needs more unit tests.

Notes for advanced setups
-------------------------

* If your are using a common Products directory, do not use the "products" directive in your zope.conf. There seems to be a known limitation (we found with a ZEO setup), preventing you from using the "container-class" definition variable. Instead, use the symlink technique to have your Zope(s) share the same Products directory.

