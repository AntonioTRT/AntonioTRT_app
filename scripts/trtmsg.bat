@echo off
REM Script wrapper para ejecutar trtmsg desde el root
REM Uso: trtmsg version
REM       trtmsg help
REM       trtmsg send LED_ON 1

cd /d "%~dp0.."

if not exist ".venv\Scripts\python.exe" (
    echo Error: Virtual environment no encontrado.
    echo Por favor ejecuta: python -m venv .venv
    exit /b 1
)

.venv\Scripts\python.exe core/trtmsg.py %*
