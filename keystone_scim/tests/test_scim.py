import uuid

from keystone import config
from keystone_scim.contrib.scim import controllers
from keystone.tests import test_v3
import keystone.tests.core as core
import os

CONF = config.CONF

# Monkey-patch Keystone test utils
core.TESTSDIR = os.path.dirname(os.path.abspath(__file__))
core.ROOTDIR = os.path.normpath(os.path.join(core.TESTSDIR, '..', '..'))
core.ETCDIR = os.path.join(core.ROOTDIR, 'etc')


class BaseCRUDTests(object):

    EXTENSION_NAME = 'scim'
    EXTENSION_TO_ADD = 'scim_extension'

#    def setUp(self):
#        super(BaseCRUDTests, self).setUp()
#        self.base_url = 'http://localhost/v3'
#        self.controller = controllers.ScimUserV3Controller()

    def build_entity(self, *args, **kwarws):
        raise NotImplementedError

    def proto_entity(self, *args, **kwarws):
        raise NotImplementedError

    def modify(self, entity):
        raise NotImplementedError

    def test_create(self):
        name = uuid.uuid4().hex
        entity = self.build_entity(name, self.domain_id)
        resp = self.post(self.URL, body=entity).result

        self.assertIsNotNone(resp['id'])

        expected_entity = self.proto_entity(name, self.domain_id,
                                            ref_id=resp['id'])

        self.assertEqual(expected_entity, resp)

    def test_list(self):
        name = uuid.uuid4().hex
        entity = self.build_entity(name, self.domain_id)
        self.post(self.URL, body=entity)

        URL = ('%(base)s?domain_id=%(domain_id)s' %
               {'base': self.URL, 'domain_id': self.domain_id})
        entities = self.get(URL).result
        matching_listed = [u for u in entities['Resources']
                           if u.get(self.NAME, '') == name]

        self.assertEqual(1, len(matching_listed))

        expected_entity = self.proto_entity(name, self.domain_id,
            ref_id=matching_listed[0]['id'], remove=['schemas'])
        self.assertEqual(expected_entity, matching_listed[0])

    def test_get(self):
        name = uuid.uuid4().hex
        entity = self.build_entity(name, self.domain_id)
        resp = self.post(self.URL, body=entity).result

        entity_url = '%s/%s' % (self.URL, resp['id'])
        got_entity = self.get(entity_url).result

        expected_entity = self.proto_entity(name, self.domain_id,
                                            ref_id=resp['id'])

        self.assertEqual(expected_entity, got_entity)

    def test_update(self):
        name = uuid.uuid4().hex
        entity = self.build_entity(name, self.domain_id)
        resp = self.post(self.URL, body=entity).result

        modified_entity = self.modify(resp)

        entity_url = '%s/%s' % (self.URL, resp['id'])
        self.put(entity_url, body=modified_entity, expected_status=200)
        got_entity = self.get(entity_url).result

        self.assertEqual(modified_entity, got_entity)

    def test_delete(self):
        name = uuid.uuid4().hex
        entity = self.build_entity(name, self.domain_id)
        resp = self.post(self.URL, body=entity).result

        entity_url = '%s/%s' % (self.URL, resp['id'])
        self.delete(entity_url, expected_status=204)
        self.get(entity_url, expected_status=404)


class RolesTests(test_v3.RestfulTestCase, BaseCRUDTests):

    URL = '/OS-SCIM/Roles'
    NAME = 'name'

    def setUp(self):
        super(RolesTests, self).setUp()
        self.base_url = 'http://localhost/v3'
        self.controller = controllers.ScimRoleV3Controller()

    def build_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        proto = {
            'schemas': ['urn:scim:schemas:extension:keystone:1.0'],
            'name': name,
            'domain_id': domain,
            'id': ref_id
        }
        return dict((key, value)
                    for key, value in proto.iteritems()
                    if value is not None and key not in remove)

    def proto_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        return self.build_entity(name, domain, ref_id, remove)

    def modify(self, entity):
        modified_entity = entity.copy()
        modified_entity['name'] = uuid.uuid4().hex
        return modified_entity


class UsersTests(test_v3.RestfulTestCase, BaseCRUDTests):

    URL = '/OS-SCIM/Users'
    NAME = 'userName'

    def setUp(self):
        super(UsersTests, self).setUp()
        self.base_url = 'http://localhost/v3'
        self.controller = controllers.ScimUserV3Controller()

    def build_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        proto = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'userName': name,
            'password': 'password',
            'id': ref_id,
            'emails': [
                {
                    'value': '%s@mailhost.com' % name
                }
            ],
            'active': True,
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': domain
            }
        }
        return dict((key, value)
                    for key, value in proto.iteritems()
                    if value is not None and key not in remove)

    def proto_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        entity = self.build_entity(name, domain, ref_id, remove)
        entity.pop('password')
        return entity

    def modify(self, entity):
        modified_entity = entity.copy()
        modified_entity['emails'][0]['value'] = \
            '%s@mailhost.com' % uuid.uuid4().hex
        return modified_entity


class GroupsTests(test_v3.RestfulTestCase, BaseCRUDTests):

    URL = '/OS-SCIM/Groups'
    NAME = 'displayName'

    def setUp(self):
        super(GroupsTests, self).setUp()
        self.base_url = 'http://localhost/v3'
        self.controller = controllers.ScimGroupV3Controller()

    def build_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        proto = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'displayName': name,
            'id': ref_id,
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': domain
            }
        }
        return dict((key, value)
                    for key, value in proto.iteritems()
                    if value is not None and key not in remove)

    def proto_entity(self, name=None, domain=None, ref_id=None, remove=[]):
        return self.build_entity(name, domain, ref_id, remove)

    def modify(self, entity):
        modified_entity = entity.copy()
        modified_entity['displayName'] = uuid.uuid4().hex
        return modified_entity
