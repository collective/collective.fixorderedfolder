# -*- coding: utf-8 -*-
"""Setup tests for this package."""
from collective.fixorderedfolder.testing import COLLECTIVE_FIXORDEREDFOLDER_INTEGRATION_TESTING  # noqa
from plone import api
from plone.app.testing import setRoles
from plone.app.testing import TEST_USER_ID

import unittest


class TestBrokenFixed(unittest.TestCase):
    """Test that collective.fixorderedfolder is properly installed."""

    layer = COLLECTIVE_FIXORDEREDFOLDER_INTEGRATION_TESTING

    def setUp(self):
        """Custom shared utility setup for tests."""
        self.portal = self.layer['portal']
        self.installer = api.portal.get_tool('portal_quickinstaller')

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        api.content.create(self.portal, type='Folder', id='broken')
        api.content.create(self.portal.broken, type='Folder', id='sub')
        api.content.create(self.portal.broken, type='Document', id='doc')
        api.content.create(self.portal.broken.sub, type='Document', id='doc')

    def testBrokenDocumentPresent(self):
        del self.portal.broken.sub.getOrdering()._pos()['doc']
        del self.portal.broken.getOrdering()._pos()['doc']
        self.assertTrue('broken' in self.portal.objectIds())
        self.assertTrue('doc' in self.portal.broken.objectIds())
        self.assertTrue('sub' in self.portal.broken.objectIds())
        self.assertTrue('doc' in self.portal.broken.sub.objectIds())
        with self.assertRaises(ValueError):
            self.portal.broken.doc.setId('renamed')
        with self.assertRaises(ValueError):
            self.portal.broken.sub.doc.setId('renamed')

        result = self.portal.restrictedTraverse('fixOrderedFolders')()
        self.assertTrue('all ok' not in result)
        result = self.portal.restrictedTraverse('fixOrderedFolders')()
        self.assertTrue('all ok' in result)
        self.portal.broken.doc.setId('renamed')
        self.portal.broken.sub.doc.setId('renamed')
        self.assertTrue('renamed' in self.portal.broken.objectIds())
        self.assertTrue('doc' not in self.portal.broken.objectIds())
        self.assertTrue('renamed' in self.portal.broken.sub.objectIds())
        self.assertTrue('doc' not in self.portal.broken.sub.objectIds())
