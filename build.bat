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

@REM call pyinstaller.exe main.win.spec
call pyinstaller.exe --onefile %HIDDEN_IMPORTS% --hidden-import=pydicom.encoders.gdcm --hidden-import=pydicom.encoders.pylibjpeg src\app\main.py 

@REM if exist dist move /y dist %APPNAME%
@REM copy settings.ini %APPNAME%
@REM copy run.bat %APPNAME%
@REM move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat
@REM powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip
@REM if exist build rmdir /s /q build
@REM if exist %APPNAME% rmdir /s /q %APPNAME%