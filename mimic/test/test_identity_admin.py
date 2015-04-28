"""
Tests for the identity admin API.
"""
from jsonschema import validate

from twisted.plugin import IPlugin
from twisted.trial.unittest import SynchronousTestCase
from twisted.web.resource import IResource

from zope.interface.verify import verifyObject

from mimic.imimic import IAPIMock
from mimic.rest import identity_admin_api as api


class IdentityAdminAPITests(SynchronousTestCase):
    """
    Tests for the identity admin API mock.
    """
    def setUp(self):
        """
        Create a identity API mock instance for testing.
        """
        self.mock = api.IdentityAdminAPI()

    def test_interface(self):
        """
        The identity admin implements the IPlugin and IAPIMock interfaces
        faithfully.
        """
        verifyObject(IAPIMock, self.mock)
        verifyObject(IPlugin, self.mock)

    def test_resource_for_region(self):
        """
        :meth:`resource_for_region` returns an identity admin resource.
        """
        store = None
        resource = self.mock.resource_for_region("REG", "prefix", store)
        verifyObject(IResource, resource)


class CreateEndpointTemplateSchemaTests(SynchronousTestCase):
    """
    Tests for the schema for endpoint template creation.
    """
    def test_validates(self):
        """
        Test simple schema validation.
        """
        body = {
            "OS-KSCATALOG:endpointTemplate": {
                "region": "North",
                "name": "Compute",
                "type": "compute",
                "publicURL": "https://compute.north.public.com/v1",
                "internalURL": "https://compute.north.internal.com/v1",
                "adminURL": "https://service-admin.com/v1",
                "versionId": "1",
                "versionInfo": "https://compute.north.public.com/v1/",
                "versionList": "https://compute.north.public.com/",
                "RAX-AUTH:tenantAlias": "{tenant}",
            }
        }
        validate(body, api.create_endpoint_template_schema)
