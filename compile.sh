#!/bin/bash

export NUITKA_CCACHE_BINARY=none

export APPNAME=MosamaticDesktop

# Clean up leftovers
rm -rf main.build ${APPNAME}

# Get Git commit ID and store in text file
echo "$(git rev-parse HEAD)" > gitcommitid.txt

# Compile Qt resources (if any)
~/.venv/MosamaticDesktop/bin/pyside6-rcc -o src/app/resources.py src/app/resources.qrc

# Build executable. This is the same command on MacOS or Windows. If you want to disable the console
# use the flag --disable-console on MacOS or --windows-disable-console on Windows. For MacOS or 
# Windows you do need to create different startup scripts
~/.venv/MosamaticDesktop/bin/python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 src/app/main.py

# Reorganize
mv main.dist ${APPNAME}
cp settings.ini ${APPNAME}
cp run.sh ${APPNAME}
cp gitcommitid.txt ${APPNAME}
mv ${APPNAME}/run.sh ${APPNAME}/${APPNAME}
chmod +x ${APPNAME}/${APPNAME}

# Build a ZIP file for the application's distribution
zip -r ${APPNAME}.zip ${APPNAME}

# Clean up
rm -rf main.build ${APPNAME}