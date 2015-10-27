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

"""SCIM Schemeas"""

import sys

SERVICE_PROVIDER_CONFIGS = {
    "schemas": "",
    'documentationUrl': 'https://github.com/telefonicaid/fiware-keystone-scim/blob/master/README.md',
    'patch': {
        'supported': True
    },
    'information': {
        "totalUsers": "",
        "totalUserOrganizations": "",
        "totalCloudOrganizations": "",
        "totalResources": "",
        "trialUsers": "",
        "basicUsers": "",
        "communityUsers": ""
    },
    'bulk': {
        'supported': False,
        'maxOperations': 0,
        'maxPayloadSize': 0
    },
    'filter': {
        'supported': True,
        'maxResults': sys.maxint
    },
    'changePassword': {
        'supported': True
    },
    'sort': {
        'supported': False
    },
    'etag': {
        'supported': False
    },
    'xmlDataFormat': {
        'supported': False
    },
    'authenticationSchemes': [
        {
            'name': 'Keytone Authentication',
            'description': 'Authentication using Keystone',
            'specUrl': 'http://specs.openstack.org/openstack/keystone-specs',
            'documentationUrl': 'http://keystone.openstack.org/',
            'type': 'keystonetoken',
            'primary': True
        }
    ]
}

SCHEMAS = [
    {
        "id": "urn:scim:schemas:core:1.0:User",
        "name": "User",
        "description": "Keystone User",
        "schema": "urn:scim:schemas:core:1.0",
        "endpoint": "/Users",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the SCIM resource as "
                    "defined by the Service Provider. Each representation of "
                    "the resource MUST include a non-empty id value. This "
                    "identifier MUST be unique across the Service Provider's "
                    "entire set of resources. It MUST be a stable, "
                    "non-reassignable identifier that does not change when the "
                    "same resource is returned in subsequent requests. The "
                    "value of the id attribute is always issued by the Service "
                    "Provider and MUST never be specified by the Service "
                    "Consumer. REQUIRED.",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "userName",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the User typically used "
                    "by the user to directly authenticate to the service "
                    "provider. Each User MUST include a non-empty userName "
                    "value. This identifier MUST be unique across the Service "
                    "Consumer's entire set of Users.  REQUIRED",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "password",
                "type": "string",
                "multiValued": False,
                "description": "The User's clear text password. This "
                    "attribute is intended to be used as a means to specify an "
                    "initial password when creating a new User or to reset an "
                    "existing User's password.",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": False,
                "caseExact": True
            },
            {
                "name": "emails",
                "type": "complex",
                "multiValued": True,
                "multiValuedAttributeChildName": "email",
                "description": "E-mail addresses for the user. The value "
                    "SHOULD be canonicalized by the Service Provider, e.g. "
                    "bjensen@example.com instead of bjensen@EXAMPLE.COM. "
                    "Canonical Type values of work, home, and other.",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": False,
                "required": False,
                "caseExact": True,
                "subAttributes": [
                    {
                        "name": "value",
                        "type": "string",
                        "multiValued": False,
                        "description": "E-mail addresses for the user. The "
                            "value SHOULD be canonicalized by the Service "
                            "Provider, e.g. bjensen@example.com instead of "
                            "bjensen@EXAMPLE.COM. Canonical Type values of "
                            "work, home, and other.",
                        "readOnly": False,
                        "required": False,
                        "caseExact": True
                    }
                ]
            },
            {
                "name": "active",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the User's"
                    "administrative status.",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": False,
                "required": False,
                "caseExact": False
            },
            {
                "name": "domain_id",
                "type": "string",
                "multiValued": False,
                "description": "User's domain",
                "schema": "urn:scim:schemas:extension:keystone:1.0",
                "readOnly": False,
                "required": True,
                "caseExact": True
            }
        ]
    },

    {
        "id": "urn:scim:schemas:core:1.0:Group",
        "name": "Group",
        "description": "Keystone Group",
        "schema": "urn:scim:schemas:core:1.0",
        "endpoint": "/Groups",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the SCIM resource",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "displayName",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the Group",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "domain_id",
                "type": "string",
                "multiValued": False,
                "description": "Role's domain",
                "schema": "urn:scim:schemas:extension:keystone:1.0",
                "readOnly": False,
                "required": True,
                "caseExact": True
            }
        ]
    },

    {
        "id": "urn:scim:schemas:extension:keystone:1.0:Role",
        "name": "Role",
        "description": "Keystone Role SCIM (domain aware)",
        "schema": "urn:scim:schemas:extension:keystone:1.0",
        "endpoint": "/Roles",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the SCIM Resource.",
                "schema": "urn:scim:schemas:core:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "name",
                "type": "string",
                "multiValued": False,
                "description": "Role name",
                "schema": "urn:scim:schemas:extension:keystone:1.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "domain_id",
                "type": "string",
                "multiValued": False,
                "description": "Role's domain",
                "schema": "urn:scim:schemas:extension:keystone:1.0",
                "readOnly": False,
                "required": True,
                "caseExact": True
            }
        ]
    },
    {
        "id": "urn:scim:schemas:core:2.0:Organization",
        "name": "Organization",
        "description": "Keystone Organization",
        "schema": "urn:scim:schemas:core:2.0",
        "endpoint": "/Organization",
        "attributes": [
            {
                "name": "id",
                "type": "string",
                "multiValued": False,
                "description": "Unique identifier for the SCIM resource",
                "schema": "urn:scim:schemas:core:2.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "name",
                "type": "string",
                "multiValued": False,
                "description": "Organization name",
                "schema": "urn:scim:schemas:core:2.0",
                "readOnly": True,
                "required": True,
                "caseExact": True
            },
            {
                "name": "description",
                "type": "string",
                "multiValued": False,
                "description": "Organization description",
                "schema": "urn:scim:schemas:core:2.0",
                "readOnly": False,
                "required": True,
                "caseExact": True
            },
            {
                "name": "active",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the User's"
                    "administrative status.",
                "schema": "urn:scim:schemas:core:2.0",
                "readOnly": False,
                "required": False,
                "caseExact": False
            },
            {
                "name": "domain_id",
                "type": "string",
                "multiValued": False,
                "description": "Organization's domain",
                "schema": "urn:scim:schemas:extension:keystone:2.0",
                "readOnly": False,
                "required": True,
                "caseExact": True
            },
            {
                "name": "is_default",
                "type": "boolean",
                "multiValued": False,
                "description": "A Boolean value indicating the Organization's"
                    "default status",
                "schema": "urn:scim:schemas:core:2.0",
                "readOnly": False,
                "required": False,
                "caseExact": False
            },
        ]
    },
]
