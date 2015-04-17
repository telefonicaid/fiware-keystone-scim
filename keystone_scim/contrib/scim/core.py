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

from keystone.common import extension


EXTENSION_DATA = {
    'name': 'OpenStack SCIM API',
    'namespace': 'https://github.com/telefonicaid/fiware-keystone-scim',
    'alias': 'OS-SCIM',
    'updated': '2014-11-17T12:00:0-00:00',
    'description': 'Openstack SCIM extension',
    'links': [
        {
            'rel': 'describedby',
            'type': 'text/html',
            'href': 'https://github.com/telefonicaid/fiware-keystone-scim/blob/master/README.md',
        }
    ]
}

extension.register_admin_extension(EXTENSION_DATA['alias'], EXTENSION_DATA)
extension.register_public_extension(EXTENSION_DATA['alias'], EXTENSION_DATA)

# Monkey patch SQL pagination

def decorate_core_limit(f):
    def limit_scim_extenstion(query, hints):
        query = f(query, hints)
        total = query.count()
        try:
            query = query.limit(hints.scim_limit)
        except AttributeError:
            pass
        try:
            query = query.offset(hints.scim_offset)
        except AttributeError:
            pass
        hints.scim_total = total
        return query
    return limit_scim_extenstion

from keystone.common.sql import core
core._limit = decorate_core_limit(core._limit)
