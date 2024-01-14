@echo off

set APPNAME=MosamaticDesktop

if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%

@REM call nuitka --standalone --mingw64 ^
@REM     --include-package=pydicom ^
@REM     --enable-plugin=pyside6 ^
@REM     --nofollow-import-to=unittest ^
@REM     --nofollow-import-to=pytest ^
@REM     src\app\main.py

@REM call pyinstaller.exe main.win.spec
call pyinstaller.exe --onefile src\app\main.py

if exist dist move /y dist %APPNAME%

copy settings.ini %APPNAME%
copy run.bat %APPNAME%
move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat

powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip

if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%