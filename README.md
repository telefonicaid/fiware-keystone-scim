# Keystone SCIM extension

Keystone SCIM is an OpenStack Keystone extension that enables the management
of User, Groups and Roles using [SCIM v1.1 standard](
http://www.simplecloud.info). As any Keystone extension, it's designed to be
installed on top of an existing Keystone installation, following Keystone
recommendations for extensions.

A brief description of SCIM:

> The SCIM standard was created to simplify user management in the cloud by
defining a schema for representing users and groups and a REST API for all
the necessary CRUD operations.

SCIM User and Group API are a direct translation of Keystone User and Group
APIs, they even share the same security policies (with the exact same names).

On the other hand, SCIM Roles are slightly different from Keystone Roles: now
SCIM Roles are _domain aware_. The extension implementation does not make
any modification to the underlying database, in order to maintain backward
compatibility with Keystone Roles API.

SCIM Roles are implemented on top of Keystone Roles, prefixing the `domain
id` to the role name. You may argue that this is a kinda of a hack, and the
relational integrity is not maintained. And that's true, but in this way the
database schema is not modified and thus the Keystone Roles API can interact
with SCIM Roles _out-of-the-box_.

## Installing

### RPM installing on RDO Openstack

Installing from RPM is pretty straightforward:

```sh
rpm -Uvh keystone-scim-*.noarch.rpm
```

Once installed you can fine-tune the permissions (out-of-the box the
installation configures the permissions to `rule:admin_required` for Role
management; User and Group management reuses the Keystone permissions).

Restart Keystone server:

```
sudo service openstack-keystone restart
```

### TGZ installaton

**TBD**

### Permissions fine tuning

As SCIM Roles are domain aware, a new set of permissions are defined, to take
care of the domain.

Sample permissions:

```
"identity:scim_get_role": "rule:admin_required"
"identity:scim_list_roles": "rule:admin_required"
"identity:scim_create_role": "rule:admin_required"
"identity:scim_update_role": "rule:admin_required"
"identity:scim_delete_role": "rule:admin_required"
"identity:scim_get_service_provider_configs": ""
"identity:scim_get_schemas": ""
```

Recommended (and tested) permissions for a Keystone domain aware configuration
(this config assumes that Keystone policies is configured using
`policy.v3cloudsample.json`):

```
"identity:scim_delete_role": "rule:cloud_admin or rule:admin_and_matching_domain_id"
"identity:scim_update_role": "rule:cloud_admin or rule:admin_and_matching_domain_id"
"identity:scim_get_role": "rule:cloud_admin or rule:admin_and_matching_domain_id"
"identity:scim_list_roles": "rule:cloud_admin or rule:admin_and_matching_domain_id"
"identity:scim_create_role": "rule:cloud_admin or rule:admin_and_matching_domain_id"
"identity:scim_get_service_provider_configs": ""
"identity:scim_get_schemas": ""
```

## Usage

SCIM extension reuses the authentication and authorization mechanisms provided
by Keystone. This document assumes that the reader has previous experience
with Keystone, but as a reference you can read more about the Keystone
Authentication and Authorization mechanism in it's
[official documentation](https://github.com/openstack/identity-api/blob/master/v3/src/markdown/identity-api-v3.md).

SCIM itself is extensively documented in
[Core Schema](http://www.simplecloud.info/specs/draft-scim-core-schema-01.html)
and in [REST API](http://www.simplecloud.info/specs/draft-scim-api-01.html).

Given that both Keystones Auth mechanisms and SCIM are document, this section
focus on running examples, not covering the full API, but giving the reader
and overview of how this extension should be used.

Creating an User:

```sh
curl http://<KEYSTONE>:5000/v3/OS-SCIM/Users \
    -s \
    -H "X-Auth-Token: <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '
{
    "schemas": ["urn:scim:schemas:core:1.0",
                "urn:scim:schemas:extension:keystone:1.0"],
    "userName": "alice",
    "password": "passw0rd",
    "emails": [
        {
            "value": "alice@mailhost.com"
        }
    ],
    "active": true,
    "urn:scim:schemas:extension:keystone:1.0": {
        "domain_id": "91d79dc2211d43a7985ebc27cdd146df"
    }
}'
```

Response:

```json
{
  "userName": "alice",
  "urn:scim:schemas:extension:keystone:1.0": {
    "domain_id": "91d79dc2211d43a7985ebc27cdd146df"
  },
  "emails": [
    {
      "value": "alice@mailhost.com"
    }
  ],
  "active": true,
  "id": "a5e8c847f7264c5a9f01a22904e3ae93",
  "schemas": [
    "urn:scim:schemas:core:1.0",
    "urn:scim:schemas:extension:keystone:1.0"
  ]
}
```

Listing Users, filtering by `domain_id`:

```sh
curl -s -X GET -H "X-Auth-Token: <TOKEN>" \
http://<KEYSTONE>:5000/v3/OS-SCIM/Users?domain_id=<DOMAIN_ID>
```

Response:

```json
{
  "Resources": [
    {
      "active": true,
      "displayName": "adm1",
      "id": "19041ee7679649879ada04417753ad4d",
      "urn:scim:schemas:extension:keystone:1.0": {
        "domain_id": "91d79dc2211d43a7985ebc27cdd146df"
      }
    }
  ],
  "schemas": [
    "urn:scim:schemas:core:1.0",
    "urn:scim:schemas:extension:keystone:1.0"
  ]
}
```

Creating Role:

```json
curl http://<KEYSTONE>:5000/v3/OS-SCIM/Roles \
    -s \
    -H "X-Auth-Token: <TOKEN>" \
    -H "Content-Type: application/json" \
    -d '
{
  "schemas": ["urn:scim:schemas:extension:keystone:1.0"],
  "name": "aRoleName",
  "domain_id": "<DOMAIN_ID>"
}'
```

Response:

```json
{
  "schemas": [
    "urn:scim:schemas:extension:keystone:1.0"
  ],
  "domain_id": "91d79dc2211d43a7985ebc27cdd146df",
  "id": "c80481d244454cc7b796d4acf8625a69",
  "name": "aRoleName"
}
```

## Building and packaging

In any OS (Linux, OSX) with a sane build environment (basically with `rpmbuild`
installed), the RPM package can be built invoking the following command:

```
sh ./package-keystone-scim.sh
```

## Hacking

Local development (by default using `sqlite`). Running a local development
server is useful to test a full featured Keystone server with SCIM extension,
and installation is straightforward following these steps:

Setup a virtualenv (highly recommended).

```sh
virtualenv .venv
```

Activate virtualenv

```sh
source .venv/bin/activate
```

Download dependencies

```sh
pip install -r requirements.txt
pip install -r test-requirements.txt
pip install tox
```

Running tests (functional and unit tests)

```sh
tox -e py27
```

Setting up local development server. First populate database (remember that
this will use `sqlite`).

```sh
keystone-manage db_sync
```

Launch server

```sh
PYTHONPATH=.:$PYTHONPATH keystone-all --config-dir etc
```

Test SCIM extension

```sh
curl http://localhost:5000/v3/OS-SCIM/ServiceProviderConfigs \
    -s \
    -H "X-Auth-Token: ADMIN"
```

The response should look like:

```json
{
  "bulk": {
    "maxPayloadSize": 0,
    "supported": false,
    "maxOperations": 0
  },
  "filter": {
    "supported": true,
    "maxResults": 9223372036854776000
  },
  "etag": {
    "supported": false
  },
  "sort": {
    "supported": false
  },
  "changePassword": {
    "supported": true
  },
  "authenticationSchemes": [
    {
      "name": "Keytone Authentication",
      "documentationUrl": "http://keystone.openstack.org/",
      "primary": true,
      "specUrl": "http://specs.openstack.org/openstack/keystone-specs",
      "type": "keystonetoken",
      "description": "Authentication using Keystone"
    }
  ],
  "documentationUrl": null,
  "xmlDataFormat": {
    "supported": false
  },
  "patch": {
    "supported": true
  }
}
```

## Known limitations and future work

* SCIM pagination is not yet implemented.
* It's unclear if SCIM standard specifies or not the format of Error messages.
  This extension reuses Keystone error messages.
* Some Keystone attributes (like User `description`) is not mapped to SCIM. It
  could have been mapped to `displayName` (and it's pretty easy to be
  implemented), but semantically does not seem to mean the same. So in case of
  any doubt we have preferred to omit attributes without a clear translation.
