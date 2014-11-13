"""Converters between SCIM JSON representation and Keystone"""
import functools

ROLE_SEP = '#'
_EXT_SCHEMA = 'urn:scim:schemas:extension:keystone:1.0'

def _remove_dict_nones(f):
    def wrapper(*args, **kwargs):
        res = f(*args, **kwargs)
        return dict(filter(lambda x: x[1], res.items()))
    return wrapper


@_remove_dict_nones
def user_key2scim(ref, schema=True):
    return {
        'schemas': ['urn:scim:schemas:core:1.0', _EXT_SCHEMA] if schema
        else None,
        'id': ref.get('id', None),
        'userName': ref.get('name', None),
        'active': ref.get('enabled', None),
        'emails': [{'value': ref['email']}] if 'email' in ref else None,
        _EXT_SCHEMA: {
            'domain_id': ref.get('domain_id', None)
        }
    }


def listusers_key2scim(ref):
    return {
        'schemas': ['urn:scim:schemas:core:1.0', _EXT_SCHEMA],
        'Resources': map(functools.partial(user_key2scim, schema=False), ref)
    }


@_remove_dict_nones
def user_scim2key(scim):
    return {
        'domain_id': scim.get(_EXT_SCHEMA, {})
            .get('domain_id', None),
        'email': scim.get('emails', [{}])[0].get('value', None),
        'id': scim.get('id', None),
        'enabled': scim.get('active', None),
        'name': scim.get('userName', None),
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
def role_key2scim(ref, schema=True):
    scim = {
        'schemas': [_EXT_SCHEMA] if schema else None,
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


def listroles_key2scim(ref):
    return {
        'schemas': [_EXT_SCHEMA],
        'Resources': map(functools.partial(role_key2scim, schema=False), ref)
    }


@_remove_dict_nones
def group_scim2key(scim):
    return {
        'domain_id': scim.get(_EXT_SCHEMA, {})
            .get('domain_id', None),
        'id': scim.get('id', None),
        'name': scim.get('displayName', None)
    }


@_remove_dict_nones
def group_key2scim(ref, schema=True):
    return {
        'schemas': ['urn:scim:schemas:core:1.0', _EXT_SCHEMA] if schema
        else None,
        'id': ref.get('id', None),
        'displayName': ref.get('name', None),
        _EXT_SCHEMA: {
            'domain_id': ref.get('domain_id', None)
        }
    }

def listgroups_key2scim(ref):
    return {
        'schemas': ['urn:scim:schemas:core:1.0', _EXT_SCHEMA],
        'Resources': map(functools.partial(group_key2scim, schema=False), ref)
    }