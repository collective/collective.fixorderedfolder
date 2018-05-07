from OFS.Folder import Folder
from Products.Five.browser import BrowserView
from plone.folder.ordered import OrderedBTreeFolderBase
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
    result = list()
    path = '/'.join(obj.getPhysicalPath())
    if isinstance(obj, Folder):
        for subobj in obj.objectValues():
            result.extend(fixObj(subobj))
    if isinstance(obj, OrderedBTreeFolderBase):
        ordering = obj.getOrdering()
        if len(ordering._pos()) != len(ordering._order()):
            for index, id in enumerate(ordering._order()):
                if id not in ordering._pos():
                    if id in obj.objectIds():
                        del ordering._order()[index]
                        ordering.notifyAdded(id)
                        result.append('%s in folder %s' % (id, path))
        if len(ordering._pos()) != len(ordering._order()):
            logger.info(
                'issue in ordering support of %s could not be fixed.' % path
            )
        for id in ordering._pos():
            if id not in ordering._order():
                logger.info(
                    'id %s exists in _pos but not in _order of folder %s.'
                    % (id, path)
                )
    return result
