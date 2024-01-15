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

SETLOCAL ENABLEDELAYEDEXPANSION
SET "HIDDEN_IMPORTS="
FOR /F "tokens=*" %%i IN (requirements.txt) DO (
    SET "HIDDEN_IMPORTS=!HIDDEN_IMPORTS! --hidden-import=%%i"
)

call pyinstaller.exe main.win.spec
@REM call pyinstaller.exe --onefile %HIDDEN_IMPORTS% --hidden-import=pydicom.encoders.gdcm --hidden-import=pydicom.encoders.pylibjpeg src\app\main.py 

if exist dist move /y dist %APPNAME%

copy settings.ini %APPNAME%

copy run.bat %APPNAME%
move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat

powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip

if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%
