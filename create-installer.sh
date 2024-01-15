#!/bin/bash

cd src/app

zip -r ../../MosamaticDesktop.zip * -x "*__pycache__/*"

cd ../../
zip MosamaticDesktopInstaller.zip MosamaticDesktop.zip install.sh run.sh requirements.txt

rm -f MosamaticDesktop.zip