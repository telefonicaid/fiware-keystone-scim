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

"""Converters between SCIM JSON representation and Keystone"""

import functools

ROLE_SEP = '#'
_EXT_SCHEMA = 'urn:scim:schemas:extension:keystone:%s'
DEFAULT_VERSION = '1.0'


def get_schema(BASE_SCHEMA, path):
    if 'v2' in path:
        version = '2.0'
    else:
        version = '1.0'
    return BASE_SCHEMA % version


def _remove_dict_nones(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        return dict(filter(lambda x: x[1], res.items()))
    return wrapper


@_remove_dict_nones
def user_key2scim(ref, path, schema=True):
    ref = {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)] if schema
        else None,
        'id': ref.get('id', None),
        'userName': ref.get('name', None),
        'displayName': ref.get('description', None),
        'active': ref.get('enabled', None),
        'emails': [{'value': ref['email']}] if 'email' in ref else None,
        get_schema(_EXT_SCHEMA, path): {
            'domain_id': ref.get('domain_id', None)
        }
    }
    return ref


def listusers_key2scim(ref, path, page_info={}):
    res = {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)],
        'Resources': map(functools.partial(user_key2scim, schema=False,
                                           path=path), ref)
    }
    res.update(page_info)
    return res


@_remove_dict_nones
def user_scim2key(scim, path):
    return {
        'domain_id': scim.get(get_schema(_EXT_SCHEMA, path), {})
            .get('domain_id', None),
        'email': scim.get('emails', [{}])[0].get('value', None),
        'id': scim.get('id', None),
        'enabled': scim.get('active', None),
        'name': scim.get('userName', None),
        'description': scim.get('displayName', None),
        'password': scim.get('password', None)
    }


@_remove_dict_nones
def role_scim2key(scim):
    keystone = {}
    keystone['id'] = scim.get('id', None)
    if scim.get('domain_id', None):
        keystone['name'] = '%s%s%s' % (
            scim.get('domain_id'), ROLE_SEP, scim.get('name', None))
    else:
        keystone['name'] = scim.get('name', None)

    return keystone


@_remove_dict_nones
def role_key2scim(ref, path=DEFAULT_VERSION, schema=True):
    scim = {
        'schemas': [get_schema(_EXT_SCHEMA, path)] if schema else None,
        'id': ref.get('id', None)
    }
    dom_name = ref.get('name', '')
    if dom_name.find(ROLE_SEP) > -1:
        (domain, name) = dom_name.split(ROLE_SEP, 1)
    else:
        (domain, name) = (None, dom_name)
    scim['name'] = name
    scim['domain_id'] = domain

    return scim


def listroles_key2scim(ref, path, page_info={}):
    res = {
        'schemas': [get_schema(_EXT_SCHEMA, path)],
        'Resources': map(functools.partial(role_key2scim, schema=False,
                                           path=path), ref)
    }
    res.update(page_info)
    return res


@_remove_dict_nones
def group_scim2key(scim, path):
    return {
        'domain_id': scim.get(get_schema(_EXT_SCHEMA, path), {})
            .get('domain_id', None),
        'id': scim.get('id', None),
        'name': scim.get('displayName', None)
    }


@_remove_dict_nones
def group_key2scim(ref, path, schema=True):
    return {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)] if schema
        else None,
        'id': ref.get('id', None),
        'displayName': ref.get('name', None),
        get_schema(_EXT_SCHEMA, path): {
            'domain_id': ref.get('domain_id', None)
        }
    }


def listgroups_key2scim(ref, path, page_info={}):
    res = {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)],
        'Resources': map(functools.partial(group_key2scim, schema=False,
                                           path=path), ref)
    }
    res.update(page_info)
    return res


@_remove_dict_nones
def organization_key2scim(ref, path, schema=True):
    return {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)] if schema
        else None,
        'id': ref.get('id', None),
        'name': ref.get('name', None),
        'description': ref.get('description', None),
        'active': ref.get('enabled', None),
        'is_default': ref.get('is_default', None),
        get_schema(_EXT_SCHEMA, path): {
            'domain_id': ref.get('domain_id', None)
        }
    }


def listorganizations_key2scim(ref, path, page_info={}):
    res = {
        'schemas': [get_schema('urn:scim:schemas:core:%s', path),
                    get_schema(_EXT_SCHEMA, path)],
        'Resources': map(functools.partial(organization_key2scim, schema=False,
                                           path=path), ref)
    }
    res.update(page_info)
    return res


@_remove_dict_nones
def organization_scim2key(scim, path):
    return {
        'domain_id': scim.get(get_schema(_EXT_SCHEMA, path), {})
            .get('domain_id', None),
        'id': scim.get('id', None),
        'enabled': scim.get('active', None),
        'name': scim.get('name', None),
        'description': scim.get('description', None),
        'is_default': scim.get('is_default', None)
    }
