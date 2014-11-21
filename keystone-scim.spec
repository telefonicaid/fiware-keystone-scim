%define timestamp %(date +"%Y%m%d%H%M%S")
Name: keystone-scim
Version: 0.2.0
Release: %{timestamp}
Summary: Keystone SCIM extension
License: Copyright 2014 Telefonica Investigación y Desarrollo, S.A.U
Distribution: noarch
Vendor: Telefonica I+D
Group: Applications/System
Packager: Telefonica I+D
Requires: openstack-keystone
autoprov: no
autoreq: no
Prefix: /opt
BuildArch: noarch

%define _target_os Linux
%define python_lib /usr/lib/python2.6/site-packages
%define keystone_paste /usr/share/keystone/keystone-dist-paste.ini
%define keystone_policy /etc/keystone/policy.json

%description
SCIM (System for Cross-domain Identity Management) extension for Keystone


%install
mkdir -p $RPM_BUILD_ROOT/%{python_lib}
cp -a %{_root}/keystone_scim $RPM_BUILD_ROOT/%{python_lib}
find $RPM_BUILD_ROOT/%{python_lib}/keystone_scim -name "*.pyc" -delete

%files
"/usr/lib/python2.6/site-packages/keystone_scim"

%post
if ! grep -q -F "[filter:scim_extension]" "%{keystone_paste}"; then
  echo "Adding SCIM extension to Keystone configuration."
  sed -i \
  -e '/^\[pipeline:api_v3\]$/,/^\[/ s/^pipeline\(.*\) service_v3$/pipeline\1 scim_extension service_v3/' \
  -e 's/\[pipeline:api_v3\]/[filter:scim_extension]\npaste.filter_factory = keystone_scim.contrib.scim.routers:ScimRouter.factory\n\n&/' \
  %{keystone_paste}
else
  echo "SCIM extension already configured. Skipping."
fi

if ! grep -q -F "identity:scim_get_role" "%{keystone_policy}"; then
  echo "Adding scim_get_role default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_get_role\"\: \"rule:admin_required\"\n/" \
    %{keystone_policy}
else
  echo "Already defined scim_get_role policy. Skipping."
fi

if ! grep -q -F "identity:scim_list_roles" "%{keystone_policy}"; then
  echo "Adding scim_list_roles default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_list_roles\"\: \"rule:admin_required\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_list_roles policy. Skipping."
fi

if ! grep -q -F "identity:scim_create_role" "%{keystone_policy}"; then
  echo "Adding scim_create_role default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_create_role\"\: \"rule:admin_required\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_create_role policy. Skipping."
fi

if ! grep -q -F "identity:scim_update_role" "%{keystone_policy}"; then
  echo "Adding scim_update_role default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_update_role\"\: \"rule:admin_required\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_update_role policy. Skipping."
fi

if ! grep -q -F "identity:scim_delete_role" "%{keystone_policy}"; then
  echo "Adding scim_delete_role default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_delete_role\"\: \"rule:admin_required\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_delete_role policy. Skipping."
fi

if ! grep -q -F "identity:scim_get_service_provider_configs" "%{keystone_policy}"; then
  echo "Adding scim_get_service_provider_configs default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_get_service_provider_configs\"\: \"\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_get_service_provider_configs. Skipping."
fi

if ! grep -q -F "identity:scim_get_schemas "%{keystone_policy}"; then
  echo "Adding scim_get_schemas default policy."
  sed -i "s/\"$/\",\n   \"identity:scim_get_schemas\"\: \"\"/" \
    %{keystone_policy}
else
  echo "Already defined scim_get_schemas. Skipping."
fi

echo "SCIM extension installed successfully. Restart Keystone daemon to take effect."

%preun
if [ $1 -gt 0 ] ; then
  # upgrading: no remove extension
  exit 0
fi
if grep -q -F "[filter:scim_extension]" "%{keystone_paste}"; then
  echo "Removing SCIM extension from Keystone configuration."
  sed -i \
  -e "/\[filter:scim_extension\]/,+2 d" \
  -e 's/scim_extension //g' \
  %{keystone_paste}
else
  echo "SCIM extension not configured. Skipping."
fi
