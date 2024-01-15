#!/bin/bash

export APPNAME=MosamaticDesktop

rm -rf build ${APPNAME}

# ~/.venv/MosamaticDesktop/bin/pyinstaller \
#     --onefile \
#     --hidden-import=pydicom.encoders.gdcm \
#     --hidden-import=pydicom.encoders.pylibjpeg \
#     src/app/main.py

hidden_imports=""
while IFS= read -r package || [[ -n "$package" ]]; do
    hidden_imports+=" --hidden-import=$package"
done < ./requirements.txt

~/.venv/MosamaticDesktop/bin/pyinstaller main.macos.spec
# ~/.venv/MosamaticDesktop/bin/pyinstaller --onefile ${hidden_imports} --hidden-import=pydicom.encoders.gdcm --hidden-import=pydicom.encoders.pylibjpeg src/app/main.py

mv dist ${APPNAME}
cp settings.ini ${APPNAME}
cp run.sh ${APPNAME}
mv ${APPNAME}/run.sh ${APPNAME}/${APPNAME}
chmod +x ${APPNAME}/${APPNAME}

zip -r ${APPNAME}.zip ${APPNAME}

rm -rf build ${APPNAME}