@echo off
setlocal

set VENV_DIR=%USERPROFILE%\.mosamatic\MosamaticDesktop

if not exist "%USERPROFILE%\.mosamatic\" mkdir "%USERPROFILE%\.mosamatic"
cd /d "%USERPROFILE%\.mosamatic"

powershell -command "Expand-Archive -Path '..\MosamaticDesktop.zip' -DestinationPath '.' -Force"

if not exist "%VENV_DIR%" (
    python -m venv "%VENV_DIR%"
)

call "%VENV_DIR%\Scripts\activate"

pip install -r requirements.txt

call "%VENV_DIR%\Scripts\deactivate.bat"
endlocal
