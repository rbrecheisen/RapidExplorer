#!/bin/bash

export APPNAME=MosamaticDesktop

rm -rf main.build ${APPNAME}

# ~/.venv/MosamaticDesktop/bin/pyinstaller \
#     --onefile \
#     --hidden-import=pydicom.encoders.gdcm \
#     --hidden-import=pydicom.encoders.pylibjpeg \
#     src/app/main.py

~/.venv/MosamaticDesktop/bin/pyinstaller main.macos.spec

mv dist ${APPNAME}
cp settings.ini ${APPNAME}
cp run.sh ${APPNAME}
mv ${APPNAME}/run.sh ${APPNAME}/${APPNAME}
chmod +x ${APPNAME}/${APPNAME}

zip -r ${APPNAME}.zip ${APPNAME}

rm -rf build ${APPNAME}