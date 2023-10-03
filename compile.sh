#!/bin/bash
rm -rf distribution
# consider using --disable-console but also requires --macos-create-app-bundle
# try this on windows as well
~/.venv/rapid/bin/python -m nuitka --enable-plugin=pyside6 --standalone src/app/main.py
mv main.dist/main.bin main.dist/rapid
mv main.dist distribution
rm -rf main.build