#
# Copyright 2014 Telefonica Investigacion y Desarrollo, S.A.U
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

"""Unit tests for SCIM converter."""

from keystone import tests
import keystone_scim.contrib.scim.converter as conv


class TestUserScimConverter(tests.BaseTestCase):

    def test_user_scim2keystone(self):
        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'userName': 'alice',
            'displayName': 'Alice Smith',
            'emails': [
                {
                    'value': 'alice@mailhost.com'
                }
            ],
            'password': 's0m3p4ssw0rd',
            'active': True,
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'description': 'Alice Smith',
            'password': 's0m3p4ssw0rd',
            'enabled': True
        }

        self.assertEqual(keystone, conv.user_scim2key(scim, path='v1'))

    def test_user_scim2keystone_no_mandatory_fields(self):
        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'userName': 'alice',
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        keystone = {
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'alice',
        }

        self.assertEqual(keystone, conv.user_scim2key(scim, path='v1'))

    def test_user_key2scim(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'description': 'Alice Smith',
            'enabled': True
        }

        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'userName': 'alice',
            'displayName': 'Alice Smith',
            'emails': [
                {
                    'value': 'alice@mailhost.com'
                }
            ],
            'active': True,
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        self.assertEqual(scim, conv.user_key2scim(keystone, path='v1'))

    def test_listusers_key2scim(self):
        page_info = {
            'path': 'v1'
        }
        keystone = [{
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'enabled': True
        }]

        scim = {
            'path': page_info['path'],
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'Resources': [{
                'id': '19041ee7679649879ada04417753ad4d',
                'userName': 'alice',
                'emails': [
                    {
                        'value': 'alice@mailhost.com'
                    }
                ],
                'active': True,
                'urn:scim:schemas:extension:keystone:1.0': {
                    'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
                }
            }]
        }


        self.assertEqual(scim, conv.listusers_key2scim(keystone, page_info))

    def test_user_key2scim_no_mandatory_fields(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
        }

        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        self.assertEqual(scim, conv.user_key2scim(keystone, path='v1'))


    def test_user_scim2key_utf8(self):
        scim = {
            'userName': u'alice',
            'urn:scim:schemas:extension:keystone:1.0': {
                u'domain_id': u'91d79dc2211d43a7985ebc27cdd146df'
            },
            'emails': [{u'value': u'alice@mailhost.com'}],
            'active': True,
            'id': u'19041ee7679649879ada04417753ad4d',
            'schemas': [u'urn:scim:schemas:core:1.0',
                        u'urn:scim:schemas:extension:keystone:1.0']}

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'email': 'alice@mailhost.com',
            'name': 'alice',
            'enabled': True
        }

        self.assertEqual(scim, conv.user_key2scim(keystone, path='v1'))

class TestRoleScimConverter(tests.BaseTestCase):

    def test_role_scim2keystone(self):
        scim = {
            'schemas': ['urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'name': 'aRole',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
        }

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'name': '%s%s%s' % ('91d79dc2211d43a7985ebc27cdd146df',
                                conv.ROLE_SEP, 'aRole')
        }

        self.assertEqual(keystone, conv.role_scim2key(scim))

    def test_role_scim2keystone_no_mandatory_fields(self):
        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'name': 'aRole'
        }

        keystone = {
            'name': 'aRole',
        }

        self.assertEqual(keystone, conv.role_scim2key(scim))

    def test_role_key2scim(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'name': '%s%s%s' % ('91d79dc2211d43a7985ebc27cdd146df',
                               conv.ROLE_SEP, 'aRole')
        }

        scim = {
            'schemas': ['urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'name': 'aRole',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
        }

        self.assertEqual(scim, conv.role_key2scim(keystone, path='v1'))

    def test_listroles_key2scim(self):
        page_info = {
            'path': 'v1'
        }
        keystone = [{
                        'id': '19041ee7679649879ada04417753ad4d',
                        'name': '%s%s%s' % ('91d79dc2211d43a7985ebc27cdd146df',
                                            conv.ROLE_SEP, 'aRole')
                    }]

        scim = {
            'path': page_info['path'],
            'schemas': ['urn:scim:schemas:extension:keystone:1.0'],
            'Resources': [{
                              'id': '19041ee7679649879ada04417753ad4d',
                              'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
                              'name': 'aRole'
                          }]
        }
        self.assertEqual(scim, conv.listroles_key2scim(keystone, page_info))


class TestGroupScimConverter(tests.BaseTestCase):

    def test_group_scim2keystone(self):
        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'displayName': 'someGroupName',
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'someGroupName'
        }

        self.assertEqual(keystone, conv.group_scim2key(scim, path='v1'))


    def test_group_key2scim(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'aGroupName'
        }

        scim = {
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'displayName': 'aGroupName',
            'urn:scim:schemas:extension:keystone:1.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        self.assertEqual(scim, conv.group_key2scim(keystone, path='v1'))

    def test_listgroups_key2scim(self):
        page_info = {
            'path': 'v1'
        }
        keystone = [{
                        'id': '19041ee7679649879ada04417753ad4d',
                        'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
                        'name': 'aGroupName'
        }]

        scim = {
            'path': page_info['path'],
            'schemas': ['urn:scim:schemas:core:1.0',
                        'urn:scim:schemas:extension:keystone:1.0'],
            'Resources': [{
                              'id': '19041ee7679649879ada04417753ad4d',
                              'displayName': 'aGroupName',
                              'urn:scim:schemas:extension:keystone:1.0': {
                                  'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
                              }
                          }]
        }
        self.assertEqual(scim, conv.listgroups_key2scim(keystone, page_info))


class TestOrganizationScimConverter(tests.BaseTestCase):

    def test_organization_scim2keystone(self):

        scim = {
            'schemas': ['urn:scim:schemas:core:2.0',
                        'urn:scim:schemas:extension:keystone:2.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'name': 'aliceOrg',
            'description': 'Alice Smith Organization',
            'active': True,
            'is_default': True,
            'urn:scim:schemas:extension:keystone:2.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'aliceOrg',
            'description': 'Alice Smith Organization',
            'is_default': True,
            'enabled': True,
        }

        self.assertEqual(keystone, conv.organization_scim2key(scim, path='v2'))

    def test_organization_scim2keystone_no_mandatory_fields(self):
        scim = {
            'schemas': ['urn:scim:schemas:core:2.0',
                        'urn:scim:schemas:extension:keystone:2.0'],
            'name': 'alice org',
            'urn:scim:schemas:extension:keystone:2.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        keystone = {
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'alice org',
        }

        self.assertEqual(keystone, conv.organization_scim2key(scim, path='v2'))

    def test_organization_key2scim(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'name': 'aliceOrg',
            'description': 'Alice Smith Organization',
            'enabled': True,
            'is_default': True
        }

        scim = {
            'schemas': ['urn:scim:schemas:core:2.0',
                        'urn:scim:schemas:extension:keystone:2.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'name': 'aliceOrg',
            'description': 'Alice Smith Organization',
            'active': True,
            'is_default': True,
            'urn:scim:schemas:extension:keystone:2.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        self.assertEqual(scim, conv.organization_key2scim(keystone, path='v2'))

    def test_listorganizations_key2scim(self):
        page_info = {
            'path': 'v2'
        }
        keystone = [{
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'description': 'Alice Organization',
            'name': 'aliceOrg',
            'enabled': True,
            'is_default': True
        }]

        scim = {
            'path': page_info['path'],
            'schemas': ['urn:scim:schemas:core:2.0',
                        'urn:scim:schemas:extension:keystone:2.0'],
            'Resources': [{
                'id': '19041ee7679649879ada04417753ad4d',
                'name': 'aliceOrg',
                'description': 'Alice Organization',
                'active': True,
                'is_default': True,
                'urn:scim:schemas:extension:keystone:2.0': {
                    'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
                }
            }]
        }
        self.assertEqual(scim, conv.listorganizations_key2scim(keystone, page_info))

    def test_organization_key2scim_no_mandatory_fields(self):
        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
        }

        scim = {
            'schemas': ['urn:scim:schemas:core:2.0',
                        'urn:scim:schemas:extension:keystone:2.0'],
            'id': '19041ee7679649879ada04417753ad4d',
            'urn:scim:schemas:extension:keystone:2.0': {
                'domain_id': '91d79dc2211d43a7985ebc27cdd146df'
            }
        }

        self.assertEqual(scim, conv.organization_key2scim(keystone, path='v2'))

    def test_organization_scim2key_utf8(self):
        scim = {
            'name': u'alice',
            'urn:scim:schemas:extension:keystone:2.0': {
                u'domain_id': u'91d79dc2211d43a7985ebc27cdd146df'
            },
            'description': u'alice org',
            'active': True,
            'is_default': True,
            'id': u'19041ee7679649879ada04417753ad4d',
            'schemas': [u'urn:scim:schemas:core:2.0',
                        u'urn:scim:schemas:extension:keystone:2.0']}

        keystone = {
            'id': '19041ee7679649879ada04417753ad4d',
            'domain_id': '91d79dc2211d43a7985ebc27cdd146df',
            'description': 'alice org',
            'name': 'alice',
            'enabled': True,
            'is_default': True
        }

        self.assertEqual(scim, conv.organization_key2scim(keystone, path='v2'))
