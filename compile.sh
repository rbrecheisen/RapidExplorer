#!/bin/bash
rm -rf distribution
# TODO:
# (1) Consider using --disable-console but also requires --macos-create-app-bundle
# (2) Try this on windows as well
~/.venv/rapid/bin/python -m nuitka --enable-plugin=pyside6 --standalone src/app/main.py
mv main.dist/main.bin main.dist/rapidx
mv main.dist distribution
rm -rf main.build