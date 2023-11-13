#!/bin/bash

PLUGINREPOSITORYDIR="src/experiments/backgroundloading/example2/plugins/repository"
PLUGINDIR="src/experiments/backgroundloading/example2/plugins/plugins"
PLUGINLIST="plugins.txt"

rm -rf ${PLUGINDIR} && mkdir ${PLUGINDIR}

cp ${PLUGINREPOSITORYDIR}/__init__.py ${PLUGINDIR}
for plugin in $(cat ${PLUGINLIST}); do
    if [[ ${plugin} =~ ^\#.* ]]; then
        continue
    fi
    pluginPath=${PLUGINDIR}/${plugin}
    mkdir -p ${pluginPath}
    cp -r ${PLUGINREPOSITORYDIR}/${plugin}/* ${pluginPath}/
    echo "Added plugin: ${pluginPath}"
done
