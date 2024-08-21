@echo off
setlocal EnableDelayedExpansion

@REM https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
@REM Also install Python 3 if needed

echo "Checking if Python 3.11 already installed..."
where python >nul 2>&1
if %ERRORLEVEL% == 0 (
    echo "Python already installed"
    goto :INSTALLMOSAMATIC
)

echo "Installing Python 3.11..."
set PYTHON_DOWNLOAD_URL=https://www.python.org/ftp/python/3.11.0/python-3.11.0-amd64.exe
set TEMP_PATH=%TEMP%\python-3.11.0-amd64.exe
powershell -Command "Invoke-WebRequest -Uri %PYTHON_DOWNLOAD_URL% -OutFile %TEMP_PATH%"
%TEMP_PATH% /quiet InstallAllUsers=1 PrependPath=1
del %TEMP_PATH%
echo "Python 3.11 installation completed"

:INSTALLMOSAMATIC

echo "Installing Mosamatic..."
set VENV_DIR=%USERPROFILE%\.mosamatic\MosamaticDesktop

echo "Creating virtual environment..."
if not exist "%USERPROFILE%\.mosamatic" mkdir "%USERPROFILE%\.mosamatic"
cd /d "%USERPROFILE%\.mosamatic"
if exist "%VENV_DIR%" rmdir /S /Q %VENV_DIR%
mkdir %VENV_DIR%
python -m venv %VENV_DIR%

echo "Installing requirements..."
call "%VENV_DIR%\Scripts\activate"
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip cache purge
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade pip
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade scikit-image
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip install mosamaticdesktop
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip install --upgrade mosamaticdesktop
%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\python -m pip install torch==2.3.1+cu121 torchvision==0.18.1+cu121 -f https://download.pytorch.org/whl/torch_stable.html
call "%VENV_DIR%\Scripts\deactivate.bat"

echo "Creating desktop shortcut for executable..."
SET ExePath=%USERPROFILE%\.mosamatic\MosamaticDesktop\Scripts\mosamatic-desktop.exe
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
del "%VBSFile%"

echo "Installation finished."
echo "You can now close this window and run Mosamatic Desktop by double-clicking the shortcut on your desktop."

endlocal
cmd