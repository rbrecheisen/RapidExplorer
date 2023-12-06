@echo off
REM Set NUITKA_CCACHE_BINARY environment variable
set NUITKA_CCACHE_BINARY=none
set APPNAME="MosamaticDesktop1.0"

REM Clean up leftovers
rmdir /s /q main.build
rmdir /s /q RapidExplorer

REM Compile Qt resources (if any)
~\.venv\RapidExplorer\Scripts\pyside6-rcc -o src\app\resources.py src\app\resources.qrc

REM Build executable. This is the same command on MacOS or Windows.
~\.venv\RapidExplorer\Scripts\python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 --nofollow-import-to=unittest src\app\main.py

REM Reorganize
move main.dist %APPNAME%
copy settings.ini %APPNAME%
copy run.bat %APPNAME%
move %APPNAME%/run.bat %APPNAME%/%APPNAME%.bat

REM Build a ZIP file for the application's distribution
powershell Compress-Archive -Path %APPNAME% -DestinationPath %APPNAME%.zip

REM Clean up
rmdir /s /q main.build
rmdir /s /q %APPNAME%
