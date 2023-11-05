#!/bin/bash

rm -rf ./RapidX

cd src/app/rapidx
~/.venv/rapidx/bin/pyside6-rcc -o resources.py resources.qrc

cd ../../../
~/.venv/rapidx/bin/python -m nuitka --include-package=pydicom --enable-plugin=pyside6 --standalone src/app/main.py

mv main.dist/main.bin main.dist/RapidX
mv main.dist RapidX

zip -r RapiX.zip RapidX

rm -rf main.build RapidX

# mkdir RapidX.app
# mkdir RapidX.app/Contents
# mkdir RapidX.app/Contents/MacOS
# mkdir RapidX.app/Contents/Resources
# cp -R distribution/* RapidX.app/Contents/MacOS
# chmod +x RapidX.app/Contents/MacOS/RapidX
# echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>" > RapidX.app/Contents/Info.plist
# echo "<!DOCTYPE plist PUBLIC \"-//Apple//DTD PLIST 1.0//EN\" \"http://www.apple.com/DTDs/PropertyList-1.0.dtd\">" >> RapidX.app/Contents/Info.plist
# echo "<plist version=\"1.0\">" >> RapidX.app/Contents/Info.plist
# echo "<dict>" >> RapidX.app/Contents/Info.plist
# echo "    <key>CFBundleExecutable</key>" >> RapidX.app/Contents/Info.plist
# echo "    <string>RapidX</string>" >> RapidX.app/Contents/Info.plist
# echo "    <key>LSMinimumSystemVersion</key>" >> RapidX.app/Contents/Info.plist
# echo "    <string>10.9</string>" >> RapidX.app/Contents/Info.plist
# echo "</dict>" >> RapidX.app/Contents/Info.plist
# echo "</plist>" >> RapidX.app/Contents/Info.plist
# hdiutil create -volname "RapidX" -srcfolder ./RapidX.app -ov -format UDZO RapidX.dmg