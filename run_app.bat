@echo off
REM Script para ejecutar la app Qt desde Windows
setlocal enabledelayedexpansion

set VENV_PYTHON=%~dp0.venv\Scripts\python.exe

if not exist "%VENV_PYTHON%" (
    echo [ERROR] venv no encontrado. Ejecuta primero:
    echo   python -m venv .venv
    echo   .venv\Scripts\pip install -r requirements.txt
    exit /b 1
)

echo [INFO] Ejecutando app con Python del venv...
"%VENV_PYTHON%" -B "%~dp0main.py"
