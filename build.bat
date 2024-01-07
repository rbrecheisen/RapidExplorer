@echo off
set APPNAME=MosamaticDesktop

if exist main.build rmdir /s /q main.build
if exist %APPNAME% rmdir /s /q %APPNAME%

call nuitka --standalone --mingw64 --include-package=pydicom --enable-plugin=pyside6 --nofollow-import-to=unittest src\app\main.py

if exist main.dist move /y main.dist %APPNAME%

copy settings.ini %APPNAME%
copy run.bat %APPNAME%
move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat

powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip

if exist main.build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%