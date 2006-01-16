
# Zope imports
from AccessControl import ClassSecurityInfo
from ComputedAttribute import ComputedAttribute
from Globals import InitializeClass
from Acquisition import aq_base
from Acquisition import aq_inner
from Acquisition import aq_parent
from ExtensionClass import Base
from OFS import ObjectManager
from zExceptions import BadRequest
from webdav.Lockable import ResourceLockedError

# CMF imports
from Products.CMFCore.utils import _checkPermission
from Products.CMFCore.utils import _getAuthenticatedUser
from Products.CMFCore import CMFCorePermissions
from Products.CMFCore.utils import getToolByName

# Archetypes imports
from Products.Archetypes.interfaces.base import IBaseFolder
from Products.Archetypes.OrderedBaseFolder import OrderedContainer

from Products.Archetypes.atapi import BaseFolderMixin
from Products.Archetypes.atapi import OrderedBaseFolder
from Products.Archetypes.atapi import registerType

# Product imports
from Products.MountFolder.config import PROJECTNAME
from Products.MountFolder.config import HAS_PLONE2

# Other imports as in ATContentTypes 0.2
if HAS_PLONE2:
    from Products.CMFPlone.PloneFolder import ReplaceableWrapper
    from webdav.NullResource import NullResource


class MountFolder(BaseFolderMixin, OrderedContainer):
    """ Special Folder to be used only for a mounted database setup inside a Plone site
        (such as our DataContent.fs). Is not referenceable.
    """

    isReferenceable = None

    __implements__ = IBaseFolder, OrderedContainer.__implements__

    schema = BaseFolderMixin.schema
    
    global_allow = 0
    use_folder_tabs = 1

    actions = ({
                'id'            : 'local_roles',
                'name'          : 'Sharing',
                'action'        : 'string:${folder_url}/folder_localrole_form',
                'permissions'   : (CMFCorePermissions.ManageProperties,),
               },)

    security = ClassSecurityInfo()

    # reference register / unregister methods
    def _register(self, *args, **kwargs): pass
    def _unregister(self, *args, **kwargs): pass
    def _updateCatalog(self, *args, **kwargs): pass
    def _referenceApply(self, *args, **kwargs): pass
    def _uncatalogUID(self, *args, **kwargs): pass
    def _uncatalogRefs(self, *args, **kwargs): pass
    
    # catalog methods
    def indexObject(self, *args, **kwargs): pass
    def unindexObject(self, *args, **kwargs): pass
    def reindexObject(self, *args, **kwargs): pass


    #
    #   FOLLOWING CODE IS COPIED FROM ATCONTENTYPES (0.2)
    #   Needed apparently for better handling of 'index_html'
    #   Fixes an ugly bug that appeared when copy/pasting a document called 'index_html'
    #
    security.declareProtected(CMFCorePermissions.View, 'index_html')
    def index_html(self):
       """Special case index_html"""
       if HAS_PLONE2:
           # COPIED FROM CMFPLONE 2.1
           request = getattr(self, 'REQUEST', None)
           if request and request.has_key('REQUEST_METHOD'):
               if (request.maybe_webdav_client and
                   request['REQUEST_METHOD'] in  ['PUT']):
                   # Very likely a WebDAV client trying to create something
                   return ReplaceableWrapper(NullResource(self, 'index_html'))
           # Acquire from parent
           _target = aq_parent(aq_inner(self)).aq_acquire('index_html')
           return ReplaceableWrapper(aq_base(_target).__of__(self))
       else:
           return OrderedBaseFolder.index_html(self)
       
    index_html = ComputedAttribute(index_html, 1)

    def __browser_default__(self, request):
        """ Set default so we can return whatever we want instead
        of index_html """
        if HAS_PLONE2:
            return getToolByName(self, 'plone_utils').browserDefault(self)
        else:
            return OrderedBaseFolder.__browser_default__(self, request)


    #
    #   FOLLOWING CODE COPIED FROM CMFCore with minor adaptation
    #   Special undo methods to fix a bug w/ CMFCore.UndoTool.py that prevents 
    #   undo-ing inner-MountFolder transactions.
    #   Improvement is needed !
    #
    security.declareProtected(CMFCorePermissions.ListUndoableChanges, 'listMFUndoableTransactionsFor')
    def listMFUndoableTransactionsFor(self, object,
                                      first_transaction=None,
                                      last_transaction=None,
                                      PrincipiaUndoBatchSize=None,
                                      #mount_folder_path='/content'
                                      ):
        """
          Lists all transaction IDs the user is allowed to undo inside the MountFolder (self).
        """
        portal = self.aq_inner.aq_parent
        #if mount_folder_path=='/content':
        #    mount_folder = portal.content
        #else:
        #    pass # FIXME
            
        transactions = self.undoable_transactions(
            first_transaction=first_transaction,
            last_transaction=last_transaction,
            PrincipiaUndoBatchSize=PrincipiaUndoBatchSize)
        for t in transactions:
            # Ensure transaction ids don't have embedded LF.
            t['id'] = t['id'].replace('\n', '')
        if not _checkPermission('Manage portal', portal):
            # Filter out transactions done by other members of the portal.
            user_id = _getAuthenticatedUser(self).getId()
            transactions = filter(
                lambda record, user_id=user_id:
                record['user_name'].split()[-1] == user_id,
                transactions
                )
        return transactions

    security.declarePublic('mf_undo')
    def mf_undo(self, object, transaction_info):
        """
            Undo the list of transactions passed in 'transaction_info',
            first verifying that the current user is allowed to undo them.
        """
        # Belt and suspenders:  make sure that the user is actually
        # allowed to undo the transation(s) in transaction_info.

        xids = {}  # set of allowed transaction IDs

        allowed = self.listMFUndoableTransactionsFor( object )

        for xid in map( lambda x: x['id'], allowed ):
            xids[xid] = 1

        if type( transaction_info ) == type( '' ):
            transaction_info = [ transaction_info ]

        for tinfo in transaction_info:
            if not xids.get( tinfo, None ):
                raise Unauthorized

        object.manage_undo_transactions(transaction_info)


registerType(MountFolder, PROJECTNAME)