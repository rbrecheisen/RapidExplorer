#!/bin/bash
cd src/${1}
~/.venv/rapid/bin/pyside6-rcc -o resources.py resources.qrc