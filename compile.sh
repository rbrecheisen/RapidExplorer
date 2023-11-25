#!/bin/bash

export NUITKA_CCACHE_BINARY=none

# Clean up leftovers
rm -rf main.build RapidExplorer

# Compile Qt resources (if any)
~/.venv/RapidExplorer/bin/pyside6-rcc -o src/app/resources.py src/app/resources.qrc

# Build executable. This is the same command on MacOS or Windows. If you want to disable the console
# use the flag --disable-console on MacOS or --windows-disable-console on Windows. For MacOS or 
# Windows you do need to create different startup scripts
~/.venv/RapidExplorer/bin/python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 src/app/main.py

# Reorganize
mv main.dist RapidExplorer
cp settings.ini RapidExplorer
cp run.sh RapidExplorer
mv RapidExplorer/run.sh RapidExplorer/RapidExplorer

# Build a ZIP file for the application's distribution
zip -r RapidExplorer.zip RapidExplorer

# Clean up
rm -rf main.build RapidExplorer