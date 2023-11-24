#!/bin/bash

export NUITKA_CCACHE_BINARY=none

# Compile Qt resources (if any)
~/.venv/RapidExplorer/bin/pyside6-rcc -o src/app/resources.py src/app/resources.qrc

# Build executable. This is the same command on MacOS or Windows. If you want to disable the console
# use the flag --disable-console on MacOS or --windows-disable-console on Windows. For MacOS or 
# Windows you do need to create different startup scripts
~/.venv/RapidExplorer/bin/python -m nuitka \
    --standalone \
    --include-data-dir=*/PythonModules \
    --include-package=pydicom \
    --enable-plugin=pyside6 \
    src/app/main.py

# Reorganize
mv main.dist/main.bin main.dist/RapidExplorer
mv main.dist RapidExplorer

# Build a ZIP file for the application's distribution
# TODO: Add a README explaining how to get it running if errors about signing occur?
zip -r RapidExplorer.zip RapidExplorer

# Clean up
rm -rf main.build RapidExplorer