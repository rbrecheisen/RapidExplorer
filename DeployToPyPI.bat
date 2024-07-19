@echo off
setlocal EnableDelayedExpansion

set PACKAGE=mosamaticdesktop

where twine >nul 2>&1
if %errorlevel% neq 0 (
  echo "You do not seem to have Twine installed (wrong venv?). It is needed to upload to PyPI"
  echo "Type 'install' to install it and continue or any other key to quit"
  set /p line=
  if not "%line%" == "install" (
    exit /b 0
  )
  python -m pip install twine wheel
)

set CMD=%1
if "%CMD%" == "-h" (
    echo "Usage: deploy.bat [patch^|minor^|major]"
    exit /b 0
)

if not "%CMD%" == "" if not "%CMD%" == "patch" if not "%CMD%" == "minor" if not "%CMD%" == "major" (
    echo "Illegal argument %CMD%"
    exit /b 1
)

if "%CMD%" == "" (
  set CMD=minor
)

for /f %%i in (VERSION) do set OLD_VERSION=%%i

python versioning.py --major-minor=%CMD%
copy VERSION .\mosamaticdesktop\VERSION
for /f %%i in (VERSION) do set VERSION=%%i

echo "Is this the right version? Type "yes" to continue, or any other key to quit."
set /p line=
if not "%line%" == "yes" (
  exit /b 0
)

git status

echo "Everything ready to be pushed to Git? Type "yes" to continue, or any other key to quit."
set /p line=
if not "%line%" == "yes" (
  exit /b 0
)

echo "Type your Git commit message here below"
set /p message=
git add -A
git commit -m "Saving version %VERSION% before deploying to PyPI. %message%"
git push

if %errorlevel% neq 0 (
    echo "Something went wrong with pushing to Git. Please revert back to previous VERSION"
    exit /b 1
)

rem GIT_COMMIT_ID=$(git log -1 --format=%%H)
rem echo %GIT_COMMIT_ID% > GIT_COMMIT_ID
rem copy GIT_COMMIT_ID .\mosamaticdesktop\GIT_COMMIT_ID

rd /s /q build
rd /s /q dist

python setup.py sdist bdist_wheel

rem twine upload --repository pypi dist/*
for /f %%i in (I:\\pypi-api.txt) do set PYPITOKEN=%%i
twine upload --username "__token__" --password "%PYPITOKEN%" --repository pypi dist\\*
