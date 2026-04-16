# 📜 Scripts - Automatización

Contiene scripts bash para instalación, compilación, flasheo y actualizaciones automáticas.

## Archivos

### install.sh
**Instalación inicial** de todas las dependencias.

```bash
./scripts/install.sh
```

Qué hace:
- ✓ Actualiza el sistema operativo
- ✓ Instala python3-serial, git, build-essential
- ✓ Instala arduino-cli y esptool.py
- ✓ Crea venv y instala requisitos Python
- ✓ Crea `config/local_config.yaml`
- ✓ Configura permisos ejecutables
- ✓ Crea alias global "trtmsg"
- ✓ Genera archivo systemd service (opcional)

**Ejecutar una sola vez por Raspberry Pi.**

### deploy.sh
**Compilación y flasheo** de firmware Arduino/ESP32.

```bash
# Default (Arduino Uno en /dev/ttyUSB0)
./scripts/deploy.sh

# Con opciones
./scripts/deploy.sh --board uno --port /dev/ttyUSB0
./scripts/deploy.sh --board esp32 --port /dev/ttyACM0
```

Opciones:
- `--board uno|esp32`: Seleccionar placa (default: uno)
- `--port /dev/ttyXXX`: Puerto série (default: /dev/ttyUSB0)

Qué hace:
1. Valida que arduino-cli esté instalado
2. Actualiza cores de Arduino
3. Compila el firmware
4. Flashea a la placa
5. Reporta estado

**Se ejecuta manualmente o**, automáticamente cuando cambia `firmware/` via `autoupdate.sh`

### autoupdate.sh
**Actualizaciones automáticas** para Raspberry Pi.

```bash
./scripts/autoupdate.sh
```

Qué hace:
1. Git fetch para ver cambios remotos
2. Compara commits local vs remoto
3. Si hay cambios:
   - Ejecuta `git pull --recurse-submodules`
   - Si cambió firmware/, flashea automáticamente
   - Si cambió requirements.txt, actualiza pip
   - Reinicia servicio `trt_ui.service`
4. Genera logs en `/tmp/trt_autoupdate.log`

**Se ejecuta periódicamente via crontab** (cada 5-10 minutos)

## Configuración Automática (Crontab)

### Instalar Watcher de Actualizaciones

1. Editar crontab:
```bash
crontab -e
```

2. Añadir una de estas líneas:

**Ejecutar cada 5 minutos:**
```bash
*/5 * * * * /home/pi/path/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
```

**Ejecutar cada 10 minutos:**
```bash
*/10 * * * * /home/pi/path/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
```

**Ejecutar diariamente a las 3 AM:**
```bash
0 3 * * * /home/pi/path/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
```

3. Guardar y salir (Ctrl+X, Enter)

### Ver Logs

```bash
# Últimas 50 líneas
tail -50 /tmp/trt_autoupdate.log

# Escuchar en tiempo real
tail -f /tmp/trt_autoupdate.log

# Buscar errores
grep ERROR /tmp/trt_autoupdate.log
```

## Servicio Systemd (Opcional)

Para que la UI arranque automáticamente:

### Generar archivo service

```bash
# El script install.sh genera /tmp/trt_ui.service
sudo cp /tmp/trt_ui.service /etc/systemd/system/
sudo systemctl daemon-reload
```

### Comandos systemd

```bash
# Habilitar servicio (auto-arranque)
sudo systemctl enable trt_ui.service

# Iniciar servicio
sudo systemctl start trt_ui.service

# Ver estado
sudo systemctl status trt_ui.service

# Ver logs
journalctl -u trt_ui.service -f

# Detener servicio
sudo systemctl stop trt_ui.service

# Reiniciar servicio
sudo systemctl restart trt_ui.service
```

## Variables de Entorno

Los scripts usan estas variables (se auto-detectan):

| Variable | Valor | Notas |
|----------|-------|-------|
| `PROJECT_ROOT` | `/home/pi/...` | Raíz del proyecto |
| `BOARD_TYPE` | `uno` \| `esp32` | De local_config.yaml |
| `SERIAL_PORT` | `/dev/ttyUSB0` | De local_config.yaml |
| `SERVICE_NAME` | `trt_ui.service` | Nombre del servicio systemd |

## Troubleshooting

### "Permission denied" al ejecutar scripts

```bash
# Dar permisos
chmod +x scripts/*.sh

# O recursivamente
chmod +x scripts/
```

### "command not found: arduino-cli"

```bash
# Reinstalar
./scripts/install.sh
```

### Crontab no funciona

1. Ver si cron está corriendo:
```bash
sudo service cron status
```

2. Verificar que el usuario pueda ejecutar crontab:
```bash
crontab -l  # Listar trabajos
```

3. Ver logs de cron:
```bash
sudo tail -f /var/log/syslog | grep CRON
```

### auto-update genera mucho log

El archivo de log se limpia automáticamente (logs > 30 días se eliminan).

Para comprimir manualmente:
```bash
gzip /tmp/trt_autoupdate.log
```

## Ejemplos Avanzados

### Flashear ESP32 con opción de bootloader

```bash
./scripts/deploy.sh --board esp32 --port /dev/ttyUSB0
# Mantén pulsado el botón BOOT durante el flasheo
```

### Ejecutar deploy.sh manualmente cada vez que cambio código

```bash
# Ver cambios
git status

# Hacer commit
git add .
git commit -m "Actualización del firmware"

# Flashear manualmente
./scripts/deploy.sh

# Push a remoto
git push origin main
```

Luego, en otra Raspberry Pi, el `autoupdate.sh` en crontab lo detectará automáticamente.

### Monitorear actualizaciones en tiempo real

```bash
# Terminal 1: Ver actualizaciones
watch -n 60 'tail /tmp/trt_autoupdate.log'

# Terminal 2: Hacer cambios y push
git push origin main

# El watcher detectará el cambio en 5-10 min (según crontab)
```

---

**Última actualización:** 2026-04-16  
**Versión:** 1.0.0
