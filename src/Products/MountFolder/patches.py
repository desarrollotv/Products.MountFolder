import Products.CMFUid.UniqueIdAnnotationTool

##################################################################################
# Monkey patch to avoid errors when the portal uid handler could not be retrieved.
##################################################################################

def handleUidAnnotationEvent(ob, event):
    """ Event subscriber for (IContentish, IObjectEvent) events
    """

    if IObjectAddedEvent.providedBy(event):
        if event.newParent is not None:
            anno_tool = queryUtility(IUniqueIdAnnotationManagement)
            uid_handler = getToolByName(ob, 'portal_uidhandler', None)
            if anno_tool is not None and uid_handler is not None:
                remove_on_add = anno_tool.getProperty('remove_on_add',False)
                remove_on_clone = anno_tool.getProperty('remove_on_clone',False)
                assign_on_add = anno_tool.getProperty('assign_on_add',False)

                if (remove_on_add and remove_on_clone) or assign_on_add:
                    try:
                        uid_handler.unregister(ob)
                    except UniqueIdError:
                        # did not have one
                        pass
                if assign_on_add:
                    # assign new uid
                    uid_handler.register(ob)

    elif IObjectClonedEvent.providedBy(event):
        anno_tool = queryUtility(IUniqueIdAnnotationManagement)
        uid_handler = getToolByName(ob, 'portal_uidhandler', None)

        if anno_tool is not None and uid_handler is not None:
            remove_on_clone = anno_tool.getProperty('remove_on_clone', False)
            assign_on_clone = anno_tool.getProperty('assign_on_clone', False)
            if remove_on_clone or assign_on_clone:
                try:
                    uid_handler.unregister(ob)
                except UniqueIdError:
                    # did not have one
                    pass
            if assign_on_clone:
                # assign new uid
                uid_handler.register(ob)



Products.CMFUid.UniqueIdAnnotationTool.handleUidAnnotationEvent = handleUidAnnotationEvent

##################################################################################
