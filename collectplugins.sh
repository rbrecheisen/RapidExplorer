#!/bin/bash

PLUGINREPOSITORY="src/app/rapidx/pluginrepository"
PLUGINLIST="plugins.txt"
PLUGINDIR="src/app/rapidx/plugins"
rm -rf ${PLUGINDIR}
mkdir ${PLUGINDIR}
cp ${PLUGINREPOSITORY}/__init__.py ${PLUGINDIR}
for plugin in $(cat ${PLUGINLIST}); do
    if [[ ${plugin} =~ ^\#.* ]]; then
        continue
    fi
    pluginPath=${PLUGINDIR}/${plugin}
    mkdir -p ${pluginPath}
    cp -r ${PLUGINREPOSITORY}/${plugin}/* ${pluginPath}/
    echo "Added plugin: ${pluginPath}"
done
