#!/usr/bin/env pwsh
# Script wrapper para ejecutar trtmsg desde PowerShell
# Uso: .\trtmsg.ps1 version
#      .\trtmsg.ps1 help
#      .\trtmsg.ps1 send LED_ON 1

$ErrorActionPreference = "Stop"

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
Set-Location (Split-Path -Parent $scriptDir)

if (-Not (Test-Path ".venv\Scripts\python.exe")) {
    Write-Host "Error: Virtual environment no encontrado."
    Write-Host "Por favor ejecuta: python -m venv .venv"
    exit 1
}

& .\.venv\Scripts\python.exe core/trtmsg.py @args
