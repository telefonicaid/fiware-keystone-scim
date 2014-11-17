#
# Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
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
    'documentationUrl': None,
    'patch': {
        'supported': True
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
        'any': None
    }
]
