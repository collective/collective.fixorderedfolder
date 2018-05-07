# -*- coding: utf-8 -*-
from plone.app.testing import FunctionalTesting
from plone.app.testing import IntegrationTesting
from plone.app.testing import PloneWithPackageLayer

import collective.fixorderedfolder


COLLECTIVE_FIXORDEREDFOLDER_FIXTURE = PloneWithPackageLayer(
    zcml_package=collective.fixorderedfolder,
    zcml_filename='testing.zcml',
    name='CollectiveFixorderedfolderLayer',
    additional_z2_products=()
)


COLLECTIVE_FIXORDEREDFOLDER_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_FIXORDEREDFOLDER_FIXTURE,),
    name='CollectiveFixorderedfolderLayer:IntegrationTesting'
)


COLLECTIVE_FIXORDEREDFOLDER_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_FIXORDEREDFOLDER_FIXTURE,),
    name='CollectiveFixorderedfolderLayer:FunctionalTesting'
)
