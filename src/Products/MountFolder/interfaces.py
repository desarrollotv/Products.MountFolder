from OFS.interfaces import IOrderedContainer
from Products.Archetypes.interfaces.base import IBaseFolder


class IMountFolder(IOrderedContainer, IBaseFolder):
    """ Mount folder to use in conjunction with ZODB Mount points.
    """
