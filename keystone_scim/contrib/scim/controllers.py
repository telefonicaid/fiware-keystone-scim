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
from keystone.assignment.controllers import ProjectV3
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
        "totalResults": hints.scim_total
    }
    if ('startIndex' in context['query_string']):
        page_info["startIndex"] = hints.scim_offset
    if ('count' in context['query_string']):
        page_info["itemsPerPage"] = hints.scim_limit
    return page_info


def get_path(path):
    if 'v2' in path:
        path = '2.0'
    elif 'v1' in path:
        path = '1.0'
    return path


@dependency.requires('assignment_api', 'identity_api')
class ScimInfoController(wsgi.Application):

    def __init__(self):
        super(ScimInfoController, self).__init__()

    def role_of(self, role_id):
        role = self.assignment_api.get_role(role_id)
        return role['name']

    def get_roles(self):
        role_user = self.assignment_api.list_role_assignments()
        basic = [u['user_id'] for u in role_user if self.role_of(u['role_id'])
                 in 'basic']
        trial = [u['user_id'] for u in role_user if self.role_of(u['role_id'])
                 in 'trial']
        community = [u['user_id'] for u in role_user
                     if self.role_of(u['role_id']) in 'community']
        basic = len(basic)
        trial = len(trial)
        community = len(community)
        return basic, trial, community

    def get_count(self):
        orgs = self.assignment_api.list_projects()
        users = self.identity_api.list_users()
        cloud_projects = [getattr(user, 'cloud_project_id', None)
                          for user in users]
        filtered_orgs = [i for i in orgs if not getattr(i, 'is_default', False)
                         and i.get('id') not in cloud_projects]
        orgs_len = len(filtered_orgs)
        cloud_len = len(cloud_projects)
        users_len = len(users)
        return orgs_len, cloud_len, users_len

    def edit_schema(self, path, schema):
        orgs, cloud, users = self.get_count()
        basic, trial, community = self.get_roles()
        schema['schemas'] = ["urn:scim:schemas:core:%s:ServiceProviderConfig"
                             % path]
        schema['information']['totalUsers'] = users
        schema['information']['totalUserOrganizations'] = orgs
        schema['information']['totalCloudOrganizations'] = cloud
        schema['information']['totalResources'] = users + orgs + cloud
        schema['information']['trialUsers'] = trial
        schema['information']['basicUsers'] = basic
        schema['information']['communityUsers'] = community
        return schema

    @controller.protected()
    def scim_get_service_provider_configs(self, context):
        path = get_path(context['path'])
        schema = schemas.SERVICE_PROVIDER_CONFIGS
        return self.edit_schema(path, schema)

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
        return conv.listusers_key2scim(refs, context['path'], scim_page_info)

    def get_user(self, context, user_id):
        ref = super(ScimUserV3Controller, self).get_user(
            context, user_id=user_id)
        return conv.user_key2scim(ref['user'], path=context['path'])

    def create_user(self, context, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        user = conv.user_scim2key(scim, path=context['path'])
        ref = super(ScimUserV3Controller, self).create_user(context, user=user)
        return conv.user_key2scim(ref.get('user', None), path=context['path'])

    def patch_user(self, context, user_id, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        user = conv.user_scim2key(scim, path=context['path'])
        ref = super(ScimUserV3Controller, self).update_user(
            context, user_id=user_id, user=user)
        return conv.user_key2scim(ref.get('user', None), path=context['path'])

    def put_user(self, context, user_id, **kwargs):
        return self.patch_user(context, user_id, **kwargs)

    def delete_user(self, context, user_id):
        return super(ScimUserV3Controller, self).delete_user(
            context, user_id=user_id)

    def _denormalize(self, data, path):
        path = get_path(path)
        data['urn:scim:schemas:extension:keystone:%s' % path] = data.pop(
            'urn_scim_schemas_extension_keystone_%s' % path, {})
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
        return conv.listroles_key2scim(refs, context['path'], scim_page_info)

    @controller.protected()
    def scim_create_role(self, context, **kwargs):
        self._require_attribute(kwargs, 'name')
        key_role = conv.role_scim2key(kwargs)
        ref = self._assign_unique_id(key_role)
        created_ref = self.assignment_api.create_role(ref['id'], ref)
        return conv.role_key2scim(created_ref, path=context['path'])

    @controller.protected()
    def scim_get_role(self, context, role_id):
        ref = self.assignment_api.get_role(role_id)
        return conv.role_key2scim(ref, path=context['path'])

    @controller.protected()
    def scim_patch_role(self, context, role_id, **role):
        key_role = conv.role_scim2key(role)
        self._require_matching_id(role_id, key_role)
        self._require_matching_domain_id(role_id, role, self.load_role)
        ref = self.assignment_api.update_role(role_id, key_role)
        return conv.role_key2scim(ref, path=context['path'])

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
        return conv.listgroups_key2scim(refs, context['path'], scim_page_info)

    def get_group(self, context, group_id):
        ref = super(ScimGroupV3Controller, self).get_group(
            context, group_id=group_id)
        return conv.group_key2scim(ref['group'], path=context['path'])

    def create_group(self, context, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        group = conv.group_scim2key(scim, path=context['path'])
        ref = super(ScimGroupV3Controller, self).create_group(
            context, group=group)
        return conv.group_key2scim(ref.get('group', None), path=context['path'])

    def patch_group(self, context, group_id, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        group = conv.group_scim2key(scim, context['path'])
        ref = super(ScimGroupV3Controller, self).update_group(
            context, group_id=group_id, group=group)
        return conv.group_key2scim(ref.get('group', None), path=context['path'])

    def put_group(self, context, group_id, **kwargs):
        return self.patch_group(context, group_id, **kwargs)

    def delete_group(self, context, group_id):
        return super(ScimGroupV3Controller, self).delete_group(
            context, group_id=group_id)
    def _denormalize(self, data, path):
        path = get_path(path)
        data['urn:scim:schemas:extension:keystone:%s' % path] = data.pop(
            'urn_scim_schemas_extension_keystone_%s' % path, {})
        return data


class ScimOrganizationV3Controller(ProjectV3):

    collection_name = 'organizations'
    member_name = 'organization'

    def __init__(self):
        super(ScimOrganizationV3Controller, self).__init__()

    @controller.filterprotected('domain_id', 'enabled', 'name')
    def list_organizations(self, context, filters):
        hints = pagination(context, ProjectV3.build_driver_hints(context, filters))
        refs = self.assignment_api.list_projects(hints=pagination(context, hints))
        scim_page_info = get_scim_page_info(context, hints)
        return conv.listorganizations_key2scim(refs, context['path'], scim_page_info)

    def get_organization(self, context, organization_id):
        ref = super(ScimOrganizationV3Controller, self).get_project(
            context, project_id=organization_id)
        return conv.organization_key2scim(ref['project'], path=context['path'])

    def create_organization(self, context, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        organization = conv.organization_scim2key(scim, path=context['path'])
        ref = super(ScimOrganizationV3Controller, self).create_project(
            context, project=organization)
        return conv.organization_key2scim(ref.get('project', None), path=context['path'])

    def patch_organization(self, context, organization_id, **kwargs):
        scim = self._denormalize(kwargs, context['path'])
        organization = conv.organization_scim2key(scim, path=context['path'])
        ref = super(ScimOrganizationV3Controller, self).update_project(
            context, project_id=organization_id, project=organization)
        return conv.organization_key2scim(ref.get('project', None), path=context['path'])

    def put_organization(self, context, organization_id, **kwargs):
        return self.patch_organization(context, organization_id, **kwargs)

    def delete_organization(self, context, organization_id):
        return super(ScimOrganizationV3Controller, self).delete_project(
            context, project_id=organization_id)

    def _denormalize(self, data, path):
        path = get_path(path)
        data['urn:scim:schemas:extension:keystone:%s' % path] = data.pop(
            'urn_scim_schemas_extension_keystone_%s' % path, {})
        return data
