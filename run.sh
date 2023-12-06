#!/bin/bash

export ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

# export GITCOMMITID="$(cat ${ROOTDIR}/gitcommitid.txt)"
# export LOGFILEPATH=${ROOTDIR}/MosamaticDesktop.log
# export SETTINGSPATH=${ROOTDIR}/settings.ini
export DATABASE=${ROOTDIR}/db.sqlite3
export DATABASEECHO=0

# ${ROOTDIR}/main.bin
${ROOTDIR}/main