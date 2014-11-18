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

        # Users

        mapper.connect(self.PATH_PREFIX + '/Users',
                       controller=user_controller,
                       action='list_users',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Users',
                       controller=user_controller,
                       action='create_user',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/Users/{user_id}',
                       controller=user_controller,
                       action='get_user',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Users/{user_id}',
                       controller=user_controller,
                       action='patch_user',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/Users/{user_id}',
                       controller=user_controller,
                       action='put_user',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/Users/{user_id}',
                       controller=user_controller,
                       action='delete_user',
                       conditions=dict(method=['DELETE']))

        # Roles

        mapper.connect(self.PATH_PREFIX + '/Roles',
                       controller=role_controller,
                       action='scim_list_roles',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Roles',
                       controller=role_controller,
                       action='scim_create_role',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_get_role',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_patch_role',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_put_role',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/Roles/{role_id}',
                       controller=role_controller,
                       action='scim_delete_role',
                       conditions=dict(method=['DELETE']))

        # Groups

        mapper.connect(self.PATH_PREFIX + '/Groups',
                       controller=group_controller,
                       action='list_groups',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Groups',
                       controller=group_controller,
                       action='create_group',
                       conditions=dict(method=['POST']))

        mapper.connect(self.PATH_PREFIX + '/Groups/{group_id}',
                       controller=group_controller,
                       action='get_group',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Groups/{group_id}',
                       controller=group_controller,
                       action='patch_group',
                       conditions=dict(method=['PATCH']))

        mapper.connect(self.PATH_PREFIX + '/Groups/{group_id}',
                       controller=group_controller,
                       action='put_group',
                       conditions=dict(method=['PUT']))

        mapper.connect(self.PATH_PREFIX + '/Groups/{group_id}',
                       controller=group_controller,
                       action='delete_group',
                       conditions=dict(method=['DELETE']))

        # SCIM Info

        mapper.connect(self.PATH_PREFIX + '/ServiceProviderConfigs',
                       controller=scim_info_controller,
                       action='scim_get_service_provider_configs',
                       conditions=dict(method=['GET']))

        mapper.connect(self.PATH_PREFIX + '/Schemas',
                       controller=scim_info_controller,
                       action='scim_get_schemas',
                       conditions=dict(method=['GET']))
