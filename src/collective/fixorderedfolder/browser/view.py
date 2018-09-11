import sys
from BTrees.OIBTree import OIBTree
from persistent.list import PersistentList
from zope.annotation.interfaces import IAnnotations
from OFS.Folder import Folder as OFSFolder
from Products.Five.browser import BrowserView
from plone.folder.ordered import OrderedBTreeFolderBase
from plone.folder.default import DefaultOrdering
import logging
logger = logging.getLogger('collective.fixorderedfolder')


class FixView(BrowserView):

    def __call__(self):
        result = list()
        result.extend(fixObj(self.context))
        if result:
            result.insert(0, 'fixed ordering support:')
            return '\n'.join(result)
        else:
            return 'all ok'


def fixObj(obj):
    """
    recursive traversal of content tree to fix all objects
    """
    result = list()
    if isinstance(obj, OrderedBTreeFolderBase):
        result.extend(fixOrderedFolder(obj))
    if isinstance(obj, OFSFolder):
        for subobj in obj.objectValues():
            result.extend(fixObj(subobj))
    return result


def fixOrderedFolder(folder):
    result = list()
    try:
        checkOrderedFolder(folder)
    except AssertionError:
        path = '/'.join(folder.getPhysicalPath())
        logger.warn(
            'Detected damage to %s. Fixing now.' % path,
            exc_info=sys.exc_info())
        try:
            ids = OrderedBTreeFolderBase.objectIds(folder)
            ordering = folder.getOrdering()
            # keep only ids that exist in underlying BTreeFolder
            # keep first id if there is more than one
            seen = list()
            for index, value in enumerate(ordering._order()):
                if value not in seen and value in ids:
                    seen.append(value)
            # add ids of objects found in BTreeFolder
            # but not in ordering
            if len(seen) < len(ids):
                for id in ids:
                    if id not in seen:
                        seen.append(id)
            # build new order list and pos dict
            order, pos = resetOrdering(ordering)
            for index, value in enumerate(seen):
                order.append(value)
                pos[value] = index
            checkOrderedFolder(folder)
            result.append('Fixed folder %s' % path)
        except: # noqa
            logger.error(
                'Failed to fix %s.' % path,
                exc_info=sys.exc_info())
            raise
        else:
            logger.info('Fixed %s.' % path)
    return result


def resetOrdering(ordering):
    annotations = IAnnotations(ordering.context)
    order = PersistentList()
    annotations.__setitem__(ordering.ORDER_KEY, order)
    pos = OIBTree()
    annotations.__setitem__(ordering.POS_KEY, pos)
    return order, pos


def checkOrderedFolder(folder):
    """check invariants
    """
    ordering = folder.getOrdering()
    if not isinstance(ordering, DefaultOrdering):
        return
    ids = OrderedBTreeFolderBase.objectIds(folder)
    order = ordering._order()
    assert len(ids) == len(order)
    assert len(set(order)) == len(order)
    assert len(ordering._pos()) == len(order)
    for index, value in enumerate(order):
        assert value in ids
        assert value in ordering._pos()
        assert ordering._pos()[value] == index
