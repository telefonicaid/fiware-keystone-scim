#!/bin/bash
#
# Packages Keystone SCIM extension as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $BASE/get_version_string.sh
#read ver rel < <(get_rpm_version_string)
string=$(get_rpm_version_string)
ver=${string% *}
rel=${string#* }

RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

rpmbuild -bb keystone-scim.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_version $ver"\
  --define "_release $rel"  
