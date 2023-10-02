#!/bin/bash
rm -rf distribution
# consider using --disable-console but also requires --macos-create-app-bundle
# try this on windows as well
~/.venv/mosamatic_desktop/bin/python -m nuitka --enable-plugin=pyside6 --standalone src/main.py
mv main.dist/main.bin main.dist/mosamatic-desktop
mv main.dist distribution
rm -rf main.build