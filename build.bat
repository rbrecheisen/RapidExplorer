@echo off

set APPNAME=MosamaticDesktop

@rem Calling executable after compiling returns with no output at all...

@REM if exist main.build rmdir /s /q main.build
if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%

@REM call nuitka --standalone --mingw64 ^
@REM     --include-package=pydicom ^
@REM     --enable-plugin=pyside6 ^
@REM     --nofollow-import-to=unittest ^
@REM     --nofollow-import-to=pytest ^
@REM     src\app\main.py

call pyinstaller main.win.spec

if exist main.dist move /y main.dist %APPNAME%

copy settings.ini %APPNAME%
copy run.bat %APPNAME%
move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat

powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip

@REM if exist main.build rmdir /s /q main.build
if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%