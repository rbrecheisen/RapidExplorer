#!/bin/bash

#Clean up left overs of previous builds
rm -rf ./RapidX

# Compile Qt resources (if any)
~/.venv/rapidx/bin/pyside6-rcc -o src/app/rapidx/resources.py src/app/rapidx/resources.qrc

# Build executable. This is the same command on MacOS or Windows. If you want to disable the console
# use the flag --disable-console on MacOS or --windows-disable-console on Windows
~/.venv/rapidx/bin/python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 src/app/main.py

# Reorganize
mv main.dist/main.bin main.dist/RapidX
mv main.dist RapidX

# Build a ZIP file for the application's distribution
# TODO: Add a README explaining how to get it running if errors about signing occur?
zip -r RapiX.zip RapidX

# Clean up
rm -rf main.build RapidX

# Build a MacOS app (not going to do that, too complicated and expensive)
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