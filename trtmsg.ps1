# Wrapper para trtmsg en PowerShell (Windows)
# Ejecuta el script real en scripts/

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
& "$scriptDir\scripts\trtmsg.ps1" @args
