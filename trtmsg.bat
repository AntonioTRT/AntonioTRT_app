@echo off
REM Wrapper para trtmsg en CMD (Windows)
REM Ejecuta el script real en scripts/

cd /d "%~dp0"
scripts\trtmsg.bat %*
