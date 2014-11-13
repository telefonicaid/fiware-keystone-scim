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
