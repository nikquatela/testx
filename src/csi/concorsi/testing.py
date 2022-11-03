# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import csi.concorsi


class CsiConcorsiLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=csi.concorsi)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'csi.concorsi:default')


CSI_CONCORSI_FIXTURE = CsiConcorsiLayer()


CSI_CONCORSI_INTEGRATION_TESTING = IntegrationTesting(
    bases=(CSI_CONCORSI_FIXTURE,),
    name='CsiConcorsiLayer:IntegrationTesting',
)


CSI_CONCORSI_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(CSI_CONCORSI_FIXTURE,),
    name='CsiConcorsiLayer:FunctionalTesting',
)


CSI_CONCORSI_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        CSI_CONCORSI_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='CsiConcorsiLayer:AcceptanceTesting',
)
