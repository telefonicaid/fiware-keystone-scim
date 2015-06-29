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

"""WSGI Routers for the SCIM API."""

from keystone.common import wsgi
import controllers


class ScimRouter(wsgi.ExtensionRouter):

    PATH_PREFIX = '/OS-SCIM'

    def add_routes(self, mapper):
        user_controller = controllers.ScimUserV3Controller()
        role_controller = controllers.ScimRoleV3Controller()
        group_controller = controllers.ScimGroupV3Controller()
        scim_info_controller = controllers.ScimInfoController()
        org_controller = controllers.ScimOrganizationV3Controller()

        # Users v1.1
        mapper.connect(self.PATH_PREFIX + '/v1/Users',
                       controller=user_controller,
                       action='list_users',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Users',
                       controller=user_controller,
                       action='create_user',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v1/Users/{user_id}',
                       controller=user_controller,
                       action='get_user',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Users/{user_id}',
                       controller=user_controller,
                       action='patch_user',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v1/Users/{user_id}',
                       controller=user_controller,
                       action='put_user',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v1/Users/{user_id}',
                       controller=user_controller,
                       action='delete_user',
                       conditions=dict(method=['DELETE']))

        # Users /v2
        mapper.connect(self.PATH_PREFIX + '/v2/Users',
                       controller=user_controller,
                       action='list_users',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Users',
                       controller=user_controller,
                       action='create_user',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v2/Users/{user_id}',
                       controller=user_controller,
                       action='get_user',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Users/{user_id}',
                       controller=user_controller,
                       action='patch_user',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v2/Users/{user_id}',
                       controller=user_controller,
                       action='put_user',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v2/Users/{user_id}',
                       controller=user_controller,
                       action='delete_user',
                       conditions=dict(method=['DELETE']))

        # Roles v1.1
        mapper.connect(self.PATH_PREFIX + '/v1/Roles',
                       controller=role_controller,
                       action='scim_list_roles',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Roles',
                       controller=role_controller,
                       action='scim_create_role',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v1/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_get_role',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_patch_role',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v1/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_put_role',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v1/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_delete_role',
                       conditions=dict(method=['DELETE']))

        # Roles /v2
        mapper.connect(self.PATH_PREFIX + '/v2/Roles',
                       controller=role_controller,
                       action='scim_list_roles',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Roles',
                       controller=role_controller,
                       action='scim_create_role',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v2/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_get_role',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_patch_role',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v2/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_put_role',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v2/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_delete_role',
                       conditions=dict(method=['DELETE']))
        # Groups v1.1
        mapper.connect(self.PATH_PREFIX + '/v1/Groups',
                       controller=group_controller,
                       action='list_groups',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Groups',
                       controller=group_controller,
                       action='create_group',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v1/Groups/{group_id}',
                       controller=group_controller,
                       action='get_group',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Groups/{group_id}',
                       controller=group_controller,
                       action='patch_group',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v1/Groups/{group_id}',
                       controller=group_controller,
                       action='put_group',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v1/Groups/{group_id}',
                       controller=group_controller,
                       action='delete_group',
                       conditions=dict(method=['DELETE']))

        # Groups
        mapper.connect(self.PATH_PREFIX + '/v2/Groups',
                       controller=group_controller,
                       action='list_groups',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Groups',
                       controller=group_controller,
                       action='create_group',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v2/Groups/{group_id}',
                       controller=group_controller,
                       action='get_group',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Groups/{group_id}',
                       controller=group_controller,
                       action='patch_group',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v2/Groups/{group_id}',
                       controller=group_controller,
                       action='put_group',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v2/Groups/{group_id}',
                       controller=group_controller,
                       action='delete_group',
                       conditions=dict(method=['DELETE']))

        # SCIM Info
        mapper.connect(self.PATH_PREFIX + '/v1/ServiceProviderConfigs',
                       controller=scim_info_controller,
                       action='scim_get_service_provider_configs',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v1/Schemas',
                       controller=scim_info_controller,
                       action='scim_get_schemas',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/ServiceProviderConfigs',
                       controller=scim_info_controller,
                       action='scim_get_service_provider_configs',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Schemas',
                       controller=scim_info_controller,
                       action='scim_get_schemas',
                       conditions=dict(method=['GET']))

        # Organizations
        mapper.connect(self.PATH_PREFIX + '/v2/Organizations',
                       controller=org_controller,
                       action='list_organizations',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Organizations',
                       controller=org_controller,
                       action='create_organization',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/v2/Organizations/{organization_id}',
                       controller=org_controller,
                       action='get_organization',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/v2/Organizations/{organization_id}',
                       controller=org_controller,
                       action='patch_organization',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/v2/Organizations/{organization_id}',
                       controller=org_controller,
                       action='put_organization',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/v2/Organizations/{organization_id}',
                       controller=org_controller,
                       action='delete_organization',
                       conditions=dict(method=['DELETE']))
