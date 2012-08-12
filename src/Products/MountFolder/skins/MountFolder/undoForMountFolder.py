## Script (Python) "undoForMountFolder"
##title=Undo transactions for MountFolder
##parameters=transaction_info, came_from
# Interim alternative to Plone's undo script
# suitable for MountFolder-based setup

mount_folder = container.portal_mountfolder.getMountFolder(context)

if mount_folder:
    mount_folder.mf_undo(context, transaction_info)
    
    msg='portal_status_message=Transaction(s)+undone.'
    
    if came_from.find('?')==-1:
        return context.REQUEST.RESPONSE.redirect( '%s?%s' % (came_from, msg) )
