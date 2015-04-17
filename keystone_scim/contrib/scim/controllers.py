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

from keystone import config
from keystone.common import controller
from keystone.common import dependency
from keystone.common import driver_hints
from keystone.common import wsgi
from keystone.identity.controllers import UserV3, GroupV3
from keystone.openstack.common import log
from keystone.openstack.common import versionutils
import converter as conv
import schemas

CONF = config.CONF
LOG = log.getLogger(__name__)


def pagination(context, hints=None):
    """Enhance Hints with SCIM pagination info (limit and offset)"""
    q = context['query_string']
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

def get_scim_page_info(context, hints):
    page_info = {
        "totalResults": hints.scim_total,
    }
    if ('startIndex' in context['query_string']):
        page_info["startIndex"] = hints.scim_offset
    if ('count' in context['query_string']):
        page_info["itemsPerPage"] = hints.scim_limit
    return page_info


class ScimInfoController(wsgi.Application):

    def __init__(self):
        super(ScimInfoController, self).__init__()

    @controller.protected()
    def scim_get_service_provider_configs(self, context):
        return schemas.SERVICE_PROVIDER_CONFIGS

    @controller.protected()
    def scim_get_schemas(self, context):
        return schemas.SCHEMAS


class ScimUserV3Controller(UserV3):

    collection_name = 'users'
    member_name = 'user'

    def __init__(self):
        super(ScimUserV3Controller, self).__init__()

    @controller.filterprotected('domain_id', 'enabled', 'name')
    def list_users(self, context, filters):
        hints = pagination(context, UserV3.build_driver_hints(context, filters))
        if 'J' in versionutils.deprecated._RELEASES:
            refs = self.identity_api.list_users(
                domain_scope=self._get_domain_id_for_list_request(context),
                hints=hints)
        else:
            refs = self.identity_api.list_users(
                domain_scope=self._get_domain_id_for_request(context),
                hints=hints)
        scim_page_info = get_scim_page_info(context, hints)
        return conv.listusers_key2scim(refs, scim_page_info)

    def get_user(self, context, user_id):
        ref = super(ScimUserV3Controller, self).get_user(
            context, user_id=user_id)
        return conv.user_key2scim(ref['user'])

    def create_user(self, context, **kwargs):
        scim = self._denormalize(kwargs)
        user = conv.user_scim2key(scim)
        ref = super(ScimUserV3Controller, self).create_user(context, user=user)
        return conv.user_key2scim(ref.get('user', None))

    def patch_user(self, context, user_id, **kwargs):
        scim = self._denormalize(kwargs)
        user = conv.user_scim2key(scim)
        ref = super(ScimUserV3Controller, self).update_user(
            context, user_id=user_id, user=user)
        return conv.user_key2scim(ref.get('user', None))

    def put_user(self, context, user_id, **kwargs):
        return self.patch_user(context, user_id, **kwargs)

    def delete_user(self, context, user_id):
        return super(ScimUserV3Controller, self).delete_user(
            context, user_id=user_id)

    def _denormalize(self, data):
        data['urn:scim:schemas:extension:keystone:1.0'] = data.pop(
            'urn_scim_schemas_extension_keystone_1.0', {})
        return data


@dependency.requires('assignment_api')
class ScimRoleV3Controller(controller.V3Controller):

    collection_name = 'roles'
    member_name = 'role'

    def __init__(self):
        super(ScimRoleV3Controller, self).__init__()
        self.get_member_from_driver = self.load_role

    @controller.filterprotected('domain_id')
    def scim_list_roles(self, context, filters):
        hints = driver_hints.Hints()
        try:
            hints.add_filter('name',
                             '%s%s' % (context['query_string']['domain_id'],
                                       conv.ROLE_SEP),
                             comparator='startswith', case_sensitive=False)
        except KeyError:
            pass
        refs = self.assignment_api.list_roles(hints=pagination(context, hints))
        scim_page_info = get_scim_page_info(context, hints)
        return conv.listroles_key2scim(refs, scim_page_info)

    @controller.protected()
    def scim_create_role(self, context, **kwargs):
        self._require_attribute(kwargs, 'name')
        key_role = conv.role_scim2key(kwargs)
        ref = self._assign_unique_id(key_role)
        created_ref = self.assignment_api.create_role(ref['id'], ref)
        return conv.role_key2scim(created_ref)

    @controller.protected()
    def scim_get_role(self, context, role_id):
        ref = self.assignment_api.get_role(role_id)
        return conv.role_key2scim(ref)

    @controller.protected()
    def scim_patch_role(self, context, role_id, **role):
        key_role = conv.role_scim2key(role)
        self._require_matching_id(role_id, key_role)
        self._require_matching_domain_id(role_id, role, self.load_role)
        ref = self.assignment_api.update_role(role_id, key_role)
        return conv.role_key2scim(ref)

    def scim_put_role(self, context, role_id, **role):
        return self.scim_patch_role(context, role_id, **role)

    def scim_delete_role(self, context, role_id):
        self.assignment_api.delete_role(role_id)

    def load_role(self, role_id):
        return conv.role_key2scim(self.assignment_api.get_role(role_id))


class ScimGroupV3Controller(GroupV3):

    collection_name = 'groups'
    member_name = 'group'

    def __init__(self):
        super(ScimGroupV3Controller, self).__init__()

    @controller.filterprotected('domain_id', 'name')
    def list_groups(self, context, filters):
        hints = pagination(context, GroupV3.build_driver_hints(context, filters))
        if 'J' in versionutils.deprecated._RELEASES:
            refs = self.identity_api.list_groups(
                domain_scope=self._get_domain_id_for_list_request(context),
                hints=hints)
        else:
            refs = self.identity_api.list_groups(
                domain_scope=self._get_domain_id_for_request(context),
                hints=hints)
        scim_page_info = get_scim_page_info(context, hints)
        return conv.listgroups_key2scim(refs, scim_page_info)

    def get_group(self, context, group_id):
        ref = super(ScimGroupV3Controller, self).get_group(
            context, group_id=group_id)
        return conv.group_key2scim(ref['group'])

    def create_group(self, context, **kwargs):
        scim = self._denormalize(kwargs)
        group = conv.group_scim2key(scim)
        ref = super(ScimGroupV3Controller, self).create_group(
            context, group=group)
        return conv.group_key2scim(ref.get('group', None))

    def patch_group(self, context, group_id, **kwargs):
        scim = self._denormalize(kwargs)
        group = conv.group_scim2key(scim)
        ref = super(ScimGroupV3Controller, self).update_group(
            context, group_id=group_id, group=group)
        return conv.group_key2scim(ref.get('group', None))

    def put_group(self, context, group_id, **kwargs):
        return self.patch_group(context, group_id, **kwargs)

    def delete_group(self, context, group_id):
        return super(ScimGroupV3Controller, self).delete_group(
            context, group_id=group_id)
    def _denormalize(self, data):
        data['urn:scim:schemas:extension:keystone:1.0'] = data.pop(
            'urn_scim_schemas_extension_keystone_1.0', {})
        return data
