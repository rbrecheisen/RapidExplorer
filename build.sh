#!/bin/bash

export APPNAME=MosamaticDesktop1.0

rm -rf main.build ${APPNAME}

# echo "$(git rev-parse HEAD)" > gitcommitid.txt

~/.venv/MosamaticDesktop/bin/pyside6-rcc -o src/app/resources.py src/app/resources.qrc
~/.venv/MosamaticDesktop/bin/pyinstaller \
    --onefile \
    --hidden-import=pydicom.encoders.gdcm \
    --hidden-import=pydicom.encoders.pylibjpeg \
    src/app/main.py

mv dist ${APPNAME}
cp settings.ini ${APPNAME}
cp run.sh ${APPNAME}
# cp gitcommitid.txt ${APPNAME}
mv ${APPNAME}/run.sh ${APPNAME}/${APPNAME}
chmod +x ${APPNAME}/${APPNAME}

zip -r ${APPNAME}.zip ${APPNAME}

rm -rf build main.spec ${APPNAME}