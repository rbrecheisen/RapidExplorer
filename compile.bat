@echo off
REM Set NUITKA_CCACHE_BINARY environment variable
set NUITKA_CCACHE_BINARY=none

REM Clean up leftovers
rmdir /s /q main.build
rmdir /s /q RapidExplorer

REM Compile Qt resources (if any)
~\.venv\RapidExplorer\Scripts\pyside6-rcc -o src\app\resources.py src\app\resources.qrc

REM Build executable. This is the same command on MacOS or Windows.
~\.venv\RapidExplorer\Scripts\python -m nuitka --standalone --include-package=pydicom --enable-plugin=pyside6 src\app\main.py

REM Reorganize
move main.dist RapidExplorer
copy settings.ini RapidExplorer
copy run.bat RapidExplorer
move RapidExplorer/run.bat RapidExplorer/RapidExplorer.bat

REM Build a ZIP file for the application's distribution
powershell Compress-Archive -Path RapidExplorer -DestinationPath RapidExplorer.zip

REM Clean up
rmdir /s /q main.build
rmdir /s /q RapidExplorer
