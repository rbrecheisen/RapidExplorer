@echo off
setlocal

@REM https://chat.openai.com/c/143bf330-901c-46ea-9115-03b450fdd07d
@REM Also install Python 3 if needed

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
