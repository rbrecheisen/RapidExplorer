@echo off

SET "SCRIPTDIR=%~dp0"
SET "SCRIPTDIR=%SCRIPTDIR:~0,-1%"
SET "DATABASE=%SCRIPTDIR%\db.sqlite3"
SET "DATABASEECHO=0"

"%SCRIPT_DIR%\main.exe"