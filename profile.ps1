# profile.ps1 - Carga funciones y aliases locales del proyecto
# Ejecutar con: . .\profile.ps1 (después de activar el venv)

function trtmsg {
    $trtmsgPath = "$(Get-Location)\trtmsg.ps1"
    if (Test-Path $trtmsgPath) {
        & $trtmsgPath @args
    } else {
        Write-Host "Error: trtmsg.ps1 no encontrado en la carpeta actual"
    }
}

Write-Host "Funciones cargadas: trtmsg"
Write-Host "Uso: trtmsg version, trtmsg help, etc."
