#!/bin/sh
#
# Packages Keystone SCIM extension as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

rpmbuild -bb keystone-scim.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"
