# Script para ejecutar la app Qt desde PowerShell
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPython = Join-Path $scriptDir ".venv\Scripts\python.exe"

if (!(Test-Path $venvPython)) {
    Write-Host "[ERROR] venv no encontrado. Ejecuta primero:" -ForegroundColor Red
    Write-Host "  python -m venv .venv"
    Write-Host "  .venv\Scripts\pip install -r requirements.txt"
    exit 1
}

Write-Host "[INFO] Ejecutando app con Python del venv..." -ForegroundColor Green
& $venvPython -B (Join-Path $scriptDir "main.py")
