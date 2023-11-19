#!/bin/bash

# Compile Qt resources (if any)
~/.venv/RapidExplorer/bin/pyside6-rcc -o src/app/resources.py src/app/resources.qrc

# Collect plugins for this build
./collectplugins.sh

# Build executable. This is the same command on MacOS or Windows. If you want to disable the console
# use the flag --disable-console on MacOS or --windows-disable-console on Windows. For MacOS or 
# Windows you do need to create different startup scripts
~/.venv/RapidExplorer/bin/python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 src/app/main.py

# Reorganize
mv main.dist/main.bin main.dist/RapidExplorer
mv main.dist RapidExplorer

# Build a ZIP file for the application's distribution
# TODO: Add a README explaining how to get it running if errors about signing occur?
zip -r RapidExplorer.zip RapidExplorer

# Clean up
rm -rf main.build RapidExplorer

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