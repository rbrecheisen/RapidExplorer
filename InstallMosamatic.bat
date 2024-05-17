@echo off
setlocal EnableDelayedExpansion

@REM https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
@REM Also install Python 3 if needed

set VENV_DIR=%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop

echo "Creating virtual environment..."
if not exist "%USERPROFILE%\Apps\Mosamatic" mkdir "%USERPROFILE%\Apps\Mosamatic"
cd /d "%USERPROFILE%\Apps\Mosamatic"
if not exist "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
)

echo "Installing requirements..."
call "%VENV_DIR%\Scripts\activate"
%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\python -m pip cache purge
%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade pip
%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade scikit-image
%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade mosamaticdesktop
call "%VENV_DIR%\Scripts\deactivate.bat"

@REM echo "Installing executable..."
@REM copy %USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\mosamatic-desktop.exe C:\Windows

echo "Creating desktop shortcut for executable..."
@REM SET ExePath=C:\Windows\mosmatic-desktop.exe
SET ExePath=%USERPROFILE%\Apps\Mosamatic\MosamaticDesktop\Scripts\mosamatic-desktop.exe
SET ShortcutName=Mosamatic Desktop

FOR /F "tokens=*" %%I IN ('reg query "HKCU\Software\Microsoft\Windows\CurrentVersion\Explorer\Shell Folders" /v Desktop') DO SET DesktopPath=%%I
SET DesktopPath=%DesktopPath:*REG_SZ=%
SET DesktopPath=%DesktopPath:~1%
SET "DesktopPath=%DesktopPath: =%"

SET VBSFile=%temp%\tempshortcut.vbs
(
echo Set oWS = WScript.CreateObject("WScript.Shell"^)
echo sLinkFile = "%DesktopPath%\%ShortcutName%.lnk"
echo Set oLink = oWS.CreateShortcut(sLinkFile^)
echo oLink.TargetPath = "%ExePath%"
echo oLink.Save
) > !VBSFile!

cscript //nologo "%VBSFile%"

@REM del "%VBSFile%"

echo "Installation finished."
echo "You can now run Mosamatic Desktop by double-clicking the shortcut on your desktop."

endlocal
cmd