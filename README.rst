===========================
collective.fixorderedfolder
===========================

``plone.folder`` maintains a data structure to support ordering.

In certain cases, that data structure can get into incoherent state.

For instance, there is a possibility that an item sitting in a folder can still
be viewed or edited but not moved or renamed.

``collective.fixorderedfolder`` provides a view (``fixOrderedFolders``) on Plone sites that walk
through the site folders to fix the case described.

Further, it logs discrepancies in the ordering data structure.
