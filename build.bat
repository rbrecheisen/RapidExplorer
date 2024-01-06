@echo off
set APPNAME=MosamaticDesktop

if exist main.build rmdir /s /q main.build
if exist %APPNAME% rmdir /s /q %APPNAME%

@REM call %USERPROFILE%\.venv\MosamaticDesktop\Scripts\pyinstaller ^
@REM     --onefile ^
@REM     --hidden-import=pydicom.encoders.gdcm ^
@REM     --hidden-import=pydicom.encoders.pylibjpeg ^
@REM     src\app\main.py

call %USERPROFILE%\.venv\MosamaticDesktop\Scripts\pyinstaller main.win.spec

if exist dist move /y dist %APPNAME%

copy settings.ini %APPNAME%
copy run.bat %APPNAME%
move /y %APPNAME%\run.bat %APPNAME%\%APPNAME%.bat

powershell Compress-Archive -Force -Path %APPNAME% -DestinationPath %APPNAME%.zip

if exist build rmdir /s /q build
if exist %APPNAME% rmdir /s /q %APPNAME%