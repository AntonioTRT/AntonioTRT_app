# trtmsg - Comando CLI para TRT

Herramienta de línea de comandos para interactuar con el sistema TRT desde PowerShell.

## Instalación Rápida

1. Activa el virtual environment:
   ```powershell
   cd D:\repos\AntonioTRT_app
   .\.venv\Scripts\Activate.ps1
   ```

2. Carga las funciones locales (una sola vez por sesión):
   ```powershell
   . .\setup-trtmsg.ps1
   ```

3. Listo. Ahora puedes usar:
   ```powershell
   trtmsg version
   trtmsg help
   ```

## Comandos Disponibles

```powershell
trtmsg version              # Muestra v1.0.0
trtmsg help                 # Muestra comandos disponibles
trtmsg send LED_ON 1        # Envía comando al microcontrolador
```

## En futuras sesiones

Simplemente vuelve a ejecutar:
```powershell
cd D:\repos\AntonioTRT_app
.\.venv\Scripts\Activate.ps1
. .\setup-trtmsg.ps1
```

O si los perfiles se cargan automáticamente, solo:
```powershell
cd D:\repos\AntonioTRT_app
.\.venv\Scripts\Activate.ps1
```

## Archivos Relacionados

- `core/trtmsg.py` - Implementación en Python
- `trtmsg.ps1` - Wrapper PowerShell
- `trtmsg.bat` - Alternativa para CMD.exe
- `setup-trtmsg.ps1` - Carga funciones en la sesión
- `Microsoft.PowerShell_profile.ps1` - Perfil global del usuario

## Solucionar Problemas

Si `trtmsg` no se reconoce:

```powershell
# Opción 1: Carga manual
. .\setup-trtmsg.ps1

# Opción 2: Verifica que estés en la carpeta correcta
Get-Location  # Debe ser: D:\repos\AntonioTRT_app

# Opción 3: Verifica que el venv está activo
# El prompt debe mostrar: (.venv) PS D:\repos\AntonioTRT_app>
```
