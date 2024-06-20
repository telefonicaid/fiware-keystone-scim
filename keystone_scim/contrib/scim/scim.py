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

"""Extensions supporting SCIM."""

from keystone.common import provider_api
from keystone.common import driver_hints
from keystone.common import rbac_enforcer
import flask
import flask_restful
from keystone.server import flask as ks_flask
from six.moves import http_client
from keystone.api.users import UserResource
from keystone.api.groups import GroupsResource
from keystone import exception
try: from oslo_log import versionutils
except ImportError: from keystone.openstack.common import versionutils
try: from oslo_log import log
except ImportError: from keystone.openstack.common import log
from keystone_scim.contrib.scim import converter as conv

try: from oslo_config import cfg
except ImportError: from oslo.config import cfg

LOG = log.getLogger(__name__)
PROVIDERS = provider_api.ProviderAPIs
ENFORCER = rbac_enforcer.RBACEnforcer

RELEASES = versionutils._RELEASES if hasattr(versionutils, '_RELEASES') else versionutils.deprecated._RELEASES


def pagination(hints=None):
    """Enhance Hints with SCIM pagination info (limit and offset)"""
    q = {
        'count': flask.request.args.get('count'),
        'startIndex': flask.request.args.get('startIndex')
    }
    if hints is None:
        hints = driver_hints.Hints()
    try:
        hints.scim_limit = q['count']
    except KeyError:
        pass
    try:
        hints.scim_offset = q['startIndex']
    except KeyError:
        pass
    return hints

def get_scim_page_info(hints):
    page_info = { "totalResults": 0 }
    try:
        page_info["totalResults"] = hints.scim_total
    except Exception:
        pass
    if flask.request.args.get('startIndex'):
        page_info["startIndex"] = hints.scim_offset
    if flask.request.args.get('count'):
        page_info["itemsPerPage"] = hints.scim_limit
    return page_info

def _build_user_target_enforcement():
    target = {}
    try:
        target['user'] = PROVIDERS.identity_api.get_user(
            flask.request.view_args.get('user_id')
        )
        if flask.request.view_args.get('group_id'):
            target['group'] = PROVIDERS.identity_api.get_group(
                flask.request.view_args.get('group_id')
            )
    except exception.NotFound:  # nosec
        # Defer existence in the event the user doesn't exist, we'll
        # check this later anyway.
        pass

    return target

def _build_group_target_enforcement():
    target = {}
    try:
        target['group'] = PROVIDERS.identity_api.get_group(
            flask.request.view_args.get('group_id')
        )
    except exception.NotFound:  # nosec
        # Defer existance in the event the group doesn't exist, we'll
        # check this later anyway.
        pass

    return target


class ScimUserResource(ks_flask.ResourceBase):
    collection_key = 'Users'
    member_key = 'user'
    api_prefix = '/OS-SCIM'
    get_member_from_driver = PROVIDERS.deferred_provider_lookup(
        api='identity_api', method='get_user')
    
    def get(self, user_id=None):
        """Get a user resource or list users.

        GET/HEAD /OS-SCIM/Users
        GET/HEAD /OS-SCIM/Users/{user_id}
        """
        if user_id is not None:
            return self._get_user(user_id)
        return self._list_users()
        
    def _list_users(self):
        filters = ('domain_id', 'enabled', 'name')
        target = None
        hints = pagination(self.build_driver_hints(filters))
        ENFORCER.enforce_call(
            action='identity:list_users', filters=filters, target_attr=target
        )
        domain = self._get_domain_id_for_list_request()
        refs = PROVIDERS.identity_api.list_users(
            domain_scope=domain, hints=hints)
        refs.sort(key=lambda d: d['name'])
        scim_page_info = get_scim_page_info(hints)
        # Fix bug retrieving from LDAP which not uses decorate_core_limit and then no scim info in hints
        if "totalResults" in scim_page_info and scim_page_info['totalResults'] == 0 and len(refs) > 0:
            scim_page_info['totalResults'] = len(refs)
            if "itemsPerPage" in scim_page_info and "startIndex" in scim_page_info:
                start = int(scim_page_info['startIndex'])
                end = int(scim_page_info['startIndex']) + int(scim_page_info['itemsPerPage'])
                refs = refs[start : end]
        res = conv.listusers_key2scim(refs, scim_page_info)
        return res

    def _get_user(self, user_id):
        ENFORCER.enforce_call(
            action='identity:get_user',
            build_target=_build_user_target_enforcement
        )
        ref = PROVIDERS.identity_api.get_user(user_id)
        wrapped = self.wrap_member(ref)
        res = conv.user_key2scim(wrapped['user'])
        LOG.debug('get_user res: %s' % res)
        return res

    def post(self):
        user_data = self.request_body_json
        target = {'user': user_data}
        ENFORCER.enforce_call(
            action='identity:create_user', target_attr=target
        )
        user_data = self._normalize_dict(user_data)
        scim = self._denormalize(user_data)
        user = conv.user_scim2key(scim)
        ref = PROVIDERS.identity_api.create_user(user)
        return conv.user_key2scim(ref.get('user', None))

    def patch(self, user_id):
        user_data = self.request_body_json
        user_data = self._normalize_dict(user_data)
        scim = self._denormalize(user_data)
        user = conv.user_scim2key(scim)
        LOG.debug('patch_user %s spasswordusercontroller' % user_id)
        ENFORCER.enforce_call(
            action='identity:update_user',
            build_target=_build_user_target_enforcement
        )
        ref = PROVIDERS.identity_api.update_user(user_id, user)
        wrapped = self.wrap_member(ref)
        return conv.user_key2scim(wrapped.get('user', None))

    def put(self, user_id):
        return self.patch_user(user_id)

    def delete(self, user_id):
        LOG.debug('delete user %s' % user_id)
        ENFORCER.enforce_call(
            action='identity:delete_user',
            build_target=_build_user_target_enforcement
        )
        PROVIDERS.identity_api.delete_user(user_id)
        return None, http_client.NO_CONTENT

    def _denormalize(self, data):
        data['urn:scim:schemas:extension:keystone:1.0'] = data.pop(
            'urn_scim_schemas_extension_keystone_1.0', {})
        return data


class ScimRoleResource(ks_flask.ResourceBase):
    collection_key = 'Roles'
    member_key = 'role'
    api_prefix = '/OS-SCIM'

    def __init__(self):
        super(ScimRoleResource, self).__init__()        
        self.get_member_from_driver = self.load_role

    def _is_domain_role(self, role):
        return bool(role.get('domain_id'))

    def get(self, role_id=None):
        """Get a role resource or list roles.

        GET/HEAD /OS-SCIM/Roles
        GET/HEAD /OS-SCIM/Roles/{user_id}
        """
        if role_id is not None:
            return self._get_role(role_id)
        return self._list_roles()

    def _list_roles(self):
        filters = ('domain_id')
        hints = driver_hints.Hints()
        hints.add_filter('name',
                         '%s%s' % (flask.request.args.get('domain_id'),
                                   conv.ROLE_SEP),
                         comparator='startswith', case_sensitive=False)
        ENFORCER.enforce_call(action='identity:list_roles',
                              filters=filters)
        refs = PROVIDERS.role_api.list_roles(hints=pagination(hints))
        #refs.sort(key=lambda d: d['name'])
        scim_page_info = get_scim_page_info(hints)
        # Fix bug retrieving from LDAP which not uses decorete_core_limit and then no scim info in in hints
        if "totalResults" in scim_page_info and scim_page_info['totalResults'] == 0 and len(refs) > 0:
            scim_page_info['totalResults'] = len(refs)
            if "itemsPerPage" in scim_page_info and "startIndex" in scim_page_info:
                start = int(scim_page_info['startIndex'])
                end = int(scim_page_info['startIndex']) + int(scim_page_info['itemsPerPage'])
                refs = refs[start : end]
        return conv.listroles_key2scim(refs, scim_page_info)

    def _get_role(self, role_id):
        err = None
        role = {}
        try:
            role = PROVIDERS.role_api.get_role(role_id)
        except Exception as e:
            err = e
        finally:
            role = self.wrap_member(role)
        return conv.role_key2scim(role)
    
    def post(self):
        role_data = self.request_body_json
        #self._require_attribute(kwargs, 'name')
        if self._is_domain_role(role_data):
            # FixMe use create_domain_role instead of create_role
            ENFORCER.enforce_call(action='identity:create_role')
        else:
            ENFORCER.enforce_call(action='identity:create_role')
        key_role = conv.role_scim2key(role_data)
        ref = self._assign_unique_id(key_role)
        ref = self._normalize_dict(ref)
        created_ref = PROVIDERS.role_api.create_role(ref['id'], ref)
        return conv.role_key2scim(created_ref), http_client.CREATED

    def patch(self, role_id):
        role_data = self.request_body_json
        err = None
        role = {}
        try:
            role = PROVIDERS.role_api.get_role(role_id)
        except Exception as e:
            err = e
        finally:
            if err is not None or not self._is_domain_role(role):
                ENFORCER.enforce_call(action='identity:update_role')
                if err:
                    raise err
            else:
                ENFORCER.enforce_call(action='identity:update_domain_role',
                                      member_target_type='role',
                                      member_target=role)
        key_role = conv.role_scim2key(role_data)
        self._require_matching_id(key_role)
        #self._require_matching_domain_id(role_id, role, self.load_role)
        ref = PROVIDERS.role_api.update_role(role_id, key_role)
        wrapped = self.wrap_member(ref)
        return conv.role_key2scim(wrapped)

    def put(self, role_id):
        return self.patch(role_id)

    def delete(self, role_id):
        err = None
        role = {}
        try:
            role = PROVIDERS.role_api.get_role(role_id)
        except Exception as e:
            err = e
        finally:
            if err is not None or not self._is_domain_role(role):
                ENFORCER.enforce_call(action='identity:delete_role')
                if err:
                    raise err
            else:
                ENFORCER.enforce_call(action='identity:delete_domain_role',
                                      member_target_type='role',
                                      member_target=role)
        PROVIDERS.role_api.delete_role(role_id)
        return None, http_client.NO_CONTENT

    def load_role(self, role_id):
        return conv.role_key2scim(PROVIDERS.role_api.get_role(role_id))


class ScimAllRoleResource(ScimRoleResource):
    api_prefix = '/OS-SCIM'
    collection_key = 'RolesAll'
    member_key = 'role'
    
    def post(self):
        ids = []
        roles_data = self.request_body_json
        for role_data in roles_data['roles']:
            #self._require_attribute(role_data, 'name')
            if self._is_domain_role(role_data):
                # FixMe use create_domain_role instead of create_role
                ENFORCER.enforce_call(action='identity:create_role')
            else:
                ENFORCER.enforce_call(action='identity:create_role')
            key_role = conv.role_scim2key(role_data)
            ref = self._assign_unique_id(key_role)
            created_ref = PROVIDERS.role_api.create_role(ref['id'], ref)
            ids.append(conv.role_key2scim(created_ref))
        return ids, http_client.CREATED

    def delete(self):
        filters = ('domain_id')
        # Get all roles of domain
        hints = driver_hints.Hints()
        hints.add_filter('name',
                         '%s%s' % (flask.request.args.get('domain_id'),
                                   conv.ROLE_SEP),
                         comparator='startswith', case_sensitive=False)
        refs = PROVIDERS.role_api.list_roles(hints=pagination(hints))
        scim_page_info = get_scim_page_info(hints)
        roles = conv.listroles_key2scim(refs, scim_page_info)
        for role in roles['Resources']:
            role_id = role['id']
            try:
                err = None
                role = {}
                role = PROVIDERS.role_api.get_role(role_id)
            except Exception as e:
                err = e
            finally:
                if err is not None or not self._is_domain_role(role):
                    ENFORCER.enforce_call(action='identity:delete_role')
                    if err:
                        raise err
                else:
                    ENFORCER.enforce_call(action='identity:delete_domain_role',
                                      member_target_type='role',
                                      member_target=role)
            # Delete each role
            PROVIDERS.role_api.delete_role(role_id)
        return None, http_client.NO_CONTENT
    
    
class ScimGroupResource(ks_flask.ResourceBase):
    collection_key = 'Groups'
    member_key = 'group'
    api_prefix = '/OS-SCIM'
    get_member_from_driver = PROVIDERS.deferred_provider_lookup(
        api='identity_api', method='get_group')

    def get(self, group_id=None):
        """Get a group resource or list groups.

        GET/HEAD /OS-SCIM/Groups
        GET/HEAD /OS-SCIM/Groups/{group_id}
        """
        if group_id is not None:
            return self._get_group(group_id)
        return self._list_groups()

    def _list_groups(self):
        filters = ('domain_id', 'name')        
        hints = pagination(self.build_driver_hints(filters))
        domain = self._get_domain_id_for_list_request()
        target = None
        ENFORCER.enforce_call(action='identity:list_groups', filters=filters,
                              target_attr=target)
        refs = PROVIDERS.identity_api.list_groups(
            domain_scope=domain, hints=hints)
        #refs.sort(key=lambda d: d['name'])
        scim_page_info = get_scim_page_info(hints)
        # Fix bug retrieving from LDAP which not uses decorete_core_limit and then no scim info in in hints
        if "totalResults" in scim_page_info and scim_page_info['totalResults'] == 0 and len(refs) > 0:
            scim_page_info['totalResults'] = len(refs)
            if "itemsPerPage" in scim_page_info and "startIndex" in scim_page_info:
                start = int(scim_page_info['startIndex'])
                end = int(scim_page_info['startIndex']) + int(scim_page_info['itemsPerPage'])
                refs = refs[start : end]
        return conv.listgroups_key2scim(refs, scim_page_info)

    def _get_group(self, group_id):
        ENFORCER.enforce_call(
            action='identity:get_group',
            build_target=_build_group_target_enforcement
        )
        ref = PROVIDERS.identity_api.get_group(group_id)
        wrapped = self.wrap_member(ref)
        return conv.group_key2scim(wrapped['group'])

    def post(self):
        group_data = self.request_body_json
        target = {'group': group_data}
        ENFORCER.enforce_call(
            action='identity:create_group', target_attr=target
        )
        scim = self._denormalize(group_data)
        group = conv.group_scim2key(scim)
        ref = PROVIDERS.identity_api.create_group(group)
        wrapped = self.wrap_member(ref)
        return conv.group_key2scim(wrapped.get('group', None))

    def patch(self, group_id):
        ENFORCER.enforce_call(
            action='identity:update_group',
            build_target=_build_group_target_enforcement
        )
        group_data = self.request_body_json
        scim = self._denormalize(group_data)
        group = conv.group_scim2key(scim)
        ref = PROVIDERS.identity_api.update_group(
            group_id, group)
        wrapped = self.wrap_member(ref)
        return conv.group_key2scim(ref.get('group', None))

    def put(self, group_id):
        return self.patch(group_id)

    def delete(self, group_id):
        ENFORCER.enforce_call(action='identity:delete_group')
        PROVIDERS.identity_api.delete_group(group_id)
        return None, http_client.NO_CONTENT

    def _denormalize(self, data):
        data['urn:scim:schemas:extension:keystone:1.0'] = data.pop(
            'urn_scim_schemas_extension_keystone_1.0', {})
        return data


class ScimAPI(ks_flask.APIBase):
    _name = 'scim'
    _import_name = __name__
    _api_url_prefix = '/OS-SCIM'
    resources = [ScimUserResource, ScimRoleResource, ScimAllRoleResource,
                 ScimGroupResource]
    resource_mapping = []

APIs = (ScimAPI,)
