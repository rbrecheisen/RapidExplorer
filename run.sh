#!/bin/bash

export ROOTDIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"

export DATABASE=${ROOTDIR}/db.sqlite3
export DATABASEECHO=0

${ROOTDIR}/main