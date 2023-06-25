#!/usr/bin/env bash

ACTOPT="$(echo ${1} | tr 'A-Z' 'a-z')"
WRKROOT=$PWD
PYCMD="${WRKROOT}/ENV/bin/python"
UTILDIR="${WRKROOT}/mkutils"

export PRJNAME=$(grep -vE '^$' PROJECT_NAME.txt | head -n 1 | sed 's/[[:space:]]//g' | tr 'A-Z' 'a-z')
PRJROOT="${PRJNAME}_expectations"


function ilog {
  local msg_str="$1"
  echo [$(date +"%F %X")]" ${msg_str}"
}


function gen_project_rootdir {
  if [ ! -d "${WRKROOT}/${PRJROOT}" ];
  then
    ilog "Generate directory ${PRJROOT}"
    mkdir "${WRKROOT}/${PRJROOT}"
    mkdir -p "${WRKROOT}/${PRJROOT}/rules"
    mkdir -p "${WRKROOT}/${PRJROOT}/data_assets"
  fi
}


function gen_manifest_file {
  echo "recursive-include ${PRJROOT} *.ini" > "${WRKROOT}/MANIFEST.in"
}


function gen_setup_file {
  if [ -f "${WRKROOT}/setup.py" ];
  then
      exit 0;
  fi

cat<<EOF> "${WRKROOT}/setup.py"
# coding=utf-8

from setuptools import setup, find_packages
import os


setup (
    name = "${PRJROOT}",
    version = "0.0.1",
    author = "xxx",
    author_email = "xxx@none.com",
    description = "Expectations for validating XXX dataset in Databricks",
    long_description = open(os.path.join(os.path.dirname(__file__), "ReadMe.md")).read(),
    long_description_content_type = "text/markdown",
    url = "https://github.com/somewhere",
    packages = find_packages(
      exclude = [
        "ENV",
        "mkutils",
        "fwtemplates"
      ]
    ),
    include_package_data=True,
    package_data = {"": ["*.ini"]},
    install_requires = open(os.path.join(os.path.dirname(__file__), "requirements.txt")).read().splitlines(),
    entry_points = {
        "console_scripts": [
            '${PRJNAME}_validate = ${PRJROOT}.main:main',
        ],
    },
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Environment :: Console",
        "Topic :: Utilities",
        "Programming Language :: Python :: 3.8",
        "Intended Audience :: Developers"
    ]
)
EOF
}


function gen_skeleton_file {
    ${PYCMD} ${UTILDIR}/copy_template_files.py --name "${PRJNAME}" --rootdir "${PRJROOT}"
}


case "${ACTOPT}" in
    "gen_root" ) gen_project_rootdir
                 ;;
    "gen_manifest" ) gen_manifest_file
                     ;;
    "gen_setup_py" ) gen_setup_file
                     ;;
    "gen_bone_files" ) gen_skeleton_file
                     ;;
    * ) ilog "Unrecognized operator !"
        exit 1
        ;;
esac

