#!/usr/bin/env pwsh
# setup-trtmsg.ps1
# Ejecutar después de activar el venv: . .\.venv\Scripts\Activate.ps1 ; . .\setup-trtmsg.ps1

# Agregar función trtmsg
function global:trtmsg {
    $trtmsgPath = "$(Get-Location)\trtmsg.ps1"
    if (Test-Path $trtmsgPath) {
        & $trtmsgPath @args
    } else {
        Write-Host "Error: trtmsg.ps1 no encontrado" -ForegroundColor Red
    }
}

Write-Host "Funcion trtmsg cargada correctamente" -ForegroundColor Green
