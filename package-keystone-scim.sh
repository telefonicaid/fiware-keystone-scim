#!/bin/bash
#
# Packages Keystone SCIM extension as RPM
#

BASE="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

source $BASE/get_version_string.sh
#read ver rel < <(get_rpm_version_string)
string=$(get_rpm_version_string)
VERSION_VALUE=${string% *}
RELEASE_VALUE=${string#* }

args=("$@")
ELEMENTS=${#args[@]}
PYTHON27_VALUE=0
PYTHON36_VALUE=0
PYTHON39_VALUE=0

for (( i=0;i<$ELEMENTS;i++)); do
    arg=${args[${i}]}
    if [ "$arg" == "--with-python27" ]; then
        PYTHON27_VALUE=1
    fi
    if [ "$arg" == "--with-python36" ]; then
        PYTHON36_VALUE=1
    fi
    if [ "$arg" == "--with-python39" ]; then
        PYTHON39_VALUE=1
    fi
    if [ "$arg" == "--with-version" ]; then
        VERSION_VALUE=${args[${i}+1]}
    fi
    if [ "$arg" == "--with-release" ]; then
        RELEASE_VALUE=${args[${i}+1]}
    fi
done

RPM_DIR=$BASE/build/rpm
mkdir -p $RPM_DIR/BUILD

rpmbuild -bb keystone-scim.spec \
  --define "_topdir $RPM_DIR" \
  --define "_root $BASE"\
  --define "_version $VERSION_VALUE"\
  --define "_release $RELEASE_VALUE"\
  --define "with_python27 $PYTHON27_VALUE"\
  --define "with_python36 $PYTHON36_VALUE"\
  --define "with_python39 $PYTHON39_VALUE"
