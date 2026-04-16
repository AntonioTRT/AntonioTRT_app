# 🔄 Guía de Actualizaciones - Sistema de Merge Inteligente

## Resumen Ejecutivo

El proyecto TRT-AntonioTRT_app tiene un **sistema automático de sincronización de configuración** que:

- ✅ **Protege valores locales** durante actualizaciones
- ✅ **Agrega nuevas variables** automáticamente  
- ✅ **Nunca sobrescribe** configuración personalizada
- ✅ **Es completamente reversible**

---

## Flujo de Instalación (Primera Vez)

```
Usuario: git clone + ./scripts/install.sh
    ↓
[install.sh]
    ├─ Instala dependencias del sistema
    ├─ Crear venv de Python
    ├─ Pip install requirements
    ├─ Ejecuta: python3 config/merge_config.py  <─── SINCRONIZACIÓN
    │   └─ local_config.yaml no existe?
    │       └─ Copia default_config.yaml → local_config.yaml
    ├─ Configura scripts ejecutables
    ├─ Crea servicio systemd (opcional)
    └─ Fin
    ↓
local_config.yaml creado (idéntico a default)
    ↓
Usuario: nano config/local_config.yaml
    └─ Personaliza valores (puerto, nombre, baudrate, etc)
```

**Resultado:** Cada Pi tiene su propia `local_config.yaml` personalizada

---

## Flujo de Actualización (Posterior)

```
Crontab: */10 * * * * ./scripts/autoupdate.sh
    ↓
[autoupdate.sh]
    ├─ git fetch (ver qué hay en remoto)
    ├─ git pull --recurse-submodules (descargar cambios)
    ├─ Ejecuta: python3 config/merge_config.py  <─── SINCRONIZACIÓN
    │   └─ Compara default vs local
    │       ├─ Nuevas claves en default?
    │       │   └─ Las agrega a local (sin perder nada)
    │       ├─ Claves existentes?
    │       │   └─ Respeta los valores locales
    │       └─ Claves desaparecidas de default?
    │           └─ Las MANTIENE en local (reversible)
    │
    ├─ Si cambió requirements.txt:
    │   └─ pip install -r requirements.txt
    │
    ├─ Si cambió firmware/:
    │   └─ ./scripts/deploy.sh (flashea placa)
    │
    ├─ systemctl restart trt_ui.service
    └─ Logs en /tmp/trt_autoupdate.log
```

**Resultado:** Local_config.yaml sincronizado sin perder valores personalizados

---

## Behavioral Examples

### Ejemplo 1: Agregar Nueva Variable

**Remoto (default_config.yaml v1.0):**
```yaml
pi_name: RaspberryPi-B
board_type: uno
serial_port: /dev/ttyUSB0
baudrate: 9600
```

**Local (tu Raspberry Pi personalizada):**
```yaml
pi_name: Mi-Garage-Automatizado
board_type: uno
serial_port: /dev/ttyACM0
baudrate: 115200
```

**El repositorio se actualiza (default_config.yaml v1.1):**
```yaml
pi_name: RaspberryPi-B
board_type: uno
serial_port: /dev/ttyUSB0
baudrate: 9600
debug_mode: false              # ← NUEVA
max_retry: 3                   # ← NUEVA
```

**Cuando corre autoupdate.sh:**

```
[merge_config.py]
├─ Lee default v1.1 (con nuevas variables)
├─ Lee local (con valores personalizados)
├─ Compara:
│  ├─ pi_name: local tiene "Mi-Garage-Automatizado" → PRESERVAR
│  ├─ board_type: local tiene "uno" → PRESERVAR  
│  ├─ serial_port: local tiene "/dev/ttyACM0" → PRESERVAR
│  ├─ baudrate: local tiene "115200" → PRESERVAR
│  ├─ debug_mode: NO EXISTE en local → AGREGAR (false)
│  └─ max_retry: NO EXISTE en local → AGREGAR (3)
└─ Guarda local actualizado

✓ RESULTADO:
pi_name: Mi-Garage-Automatizado     # ✓ Tu valor
board_type: uno
serial_port: /dev/ttyACM0           # ✓ Tu valor
baudrate: 115200                    # ✓ Tu valor
debug_mode: false                   # ✓ Nuevo, agregado automáticamente
max_retry: 3                        # ✓ Nuevo, agregado automáticamente
```

### Ejemplo 2: Actualizar Campo en Default

**Local (actualmente):**
```yaml
baudrate: 9600
```

**Remoto se actualiza a:**
```yaml
baudrate: 115200   # ← Campo "mejorado" en default
```

**Cuando corre autoupdate.sh:**

```
[merge_config.py]
├─ Lee new default (baudrate: 115200)
├─ Lee local actual (baudrate: 9600)
├─ Compara:
│  └─ baudrate: ya existe en local → PRESERVAR valor local (9600)
└─ Guarda local (sin cambios)

✓ RESULTADO:
baudrate: 9600   # ✓ TU VALOR SE MANTIENE (no se sobrescribe)
```

Si QUIERES actualizar a 115200, lo haces manualmente:
```bash
nano config/local_config.yaml
# Editar: baudrate: 115200
```

---

### Ejemplo 3: Campo Eliminado del Default

**Local (actualmente):**
```yaml
old_feature: true
pi_name: Mi-Garage
```

**Remoto se actualiza a:** (sin old_feature)
```yaml
pi_name: RaspberryPi
```

**Cuando corre autoupdate.sh:**

```
[merge_config.py]
├─ Lee new default (sin old_feature)
├─ Lee local actual (con old_feature)
├─ Compara:
│  ├─ pi_name: existe en ambos → PRESERVAR local
│  └─ old_feature: ESTÁ EN LOCAL pero NO EN DEFAULT
│      └─ Mantenerlo (es reversible si lo necesitas)
└─ Guarda local (también con old_feature)

✓ RESULTADO:
old_feature: true    # ✓ PRESERVADO (no se elimina)
pi_name: Mi-Garage   # ✓ PRESERVADO
```

Si quieres limpiar:
```bash
nano config/local_config.yaml
# Eliminar: old_feature: true
```

---

## Comandos Manuales

### Sincronizar Configuración Manualmente

```bash
# Ir a la carpeta
cd /path/to/TRT-AntonioTRT_app

# Ejecutar merge (modo verbose)
python3 config/merge_config.py

# Ejecutar merge silencioso
python3 config/merge_config.py --quiet
```

### Ver Cambios Pendientes en Remoto

```bash
# Ver qué cambios hay en GitHub sin aplicarlos
git fetch
git diff HEAD origin/main -- config/

# Ver qué pasa al hacer pull
git pull --dry-run --recurse-submodules
```

### Revertir a Default (si algo se daña)

```bash
# Respaldar actual
cp config/local_config.yaml config/local_config.yaml.bak

# Copiar default
cp config/default_config.yaml config/local_config.yaml

# Luego personalizar de nuevo
nano config/local_config.yaml
```

### Ver Historial de Actualizaciones

```bash
# Ver logs de autoupdate
tail -50 /tmp/trt_autoupdate.log

# Escuchar en tiempo real
tail -f /tmp/trt_autoupdate.log

# Buscar errores
grep ERROR /tmp/trt_autoupdate.log
```

---

## Casos de Uso

### Caso 1: Multi-Raspberry Pi con Diferentes Puertos

**Raspberry Pi B (garage):**
```yaml
pi_name: "RPi-B-Garage"
serial_port: "/dev/ttyUSB0"
```

**Raspberry Pi 5 (kitchen):**
```yaml
pi_name: "RPi-5-Kitchen"
serial_port: "/dev/ttyACM0"
baudrate: 115200
```

Cuando ambas corran `autoupdate.sh`:
- ✓ Cada una mantiene SU configuración local
- ✓ Ambas descargn los mismos cambios de código
- ✓ Ambas preservan sus valores personalizados

### Caso 2: Testing en Dev + Production

**Laptop (desarrollo):**
```yaml
debug_mode: true
max_retry: 1
serial_port: COM3
```

**Raspberry Pi (producción):**
```yaml
debug_mode: false
max_retry: 5
serial_port: /dev/ttyUSB0
```

Ambas usan el mismo código (mismo repo), pero diferente configuración.

### Caso 3: Nuevas Features Centralizadas

Tu equipo agrega una nueva feature a `default_config.yaml`:

```yaml
feature_new_lcd_support: true
lcd_brightness: 100
```

Cuando corra `autoupdate.sh` en tu Raspberry Pi:
- ✓ Descarga el código nuevo
- ✓ Automáticamente agrega `feature_new_lcd_support: true`
- ✓ Automáticamente agrega `lcd_brightness: 100`
- ✓ TUS valores personalizados (pi_name, serial_port, etc) Se preservan

---

## Troubleshooting

### "Perdí valores personalizados"

1. **Opción 1: Restaurar desde backup**
   ```bash
   cp config/local_config.yaml.bak config/local_config.yaml
   python3 config/merge_config.py
   ```

2. **Opción 2: Recrear desde default**
   ```bash
   cp config/default_config.yaml config/local_config.yaml
   nano config/local_config.yaml  # Re-personalizar
   ```

### "autoupdate.sh no ejecuta merge_config.py"

```bash
# Verificar permisos
ls -la config/merge_config.py
chmod 755 config/merge_config.py

# Ejecutar manualmente
cd /path/to/project
python3 config/merge_config.py
```

### "No sé cuáles son mis valores personalizados"

```bash
# Ver diferencia entre local y default
diff config/default_config.yaml config/local_config.yaml

# O usando `git`
git diff --no-index config/default_config.yaml config/local_config.yaml
```

---

## Reglas de Oro

| Regla | Motivo |
|-------|--------|
| **Nunca commiteës `local_config.yaml`** | Es específico de cada Pi |
| **Siempre commitea `default_config.yaml`** | Es el reference del proyecto |
| **El merge PRESERVA lo local** | Tu configuración es importante |
| **Nuevas variables se agregan solas** | As easy as possible |
| **Es reversible** | Nada se pierde permanentemente |

---

## Arquitectura del Merge

```python
# Pseudocódigo de merge_config.py

def merge(default, local):
    merged = local.copy()  # ✓ Comenzar con local
    
    for key, value in default.items():
        if key not in merged:
            # Nueva clave en default
            merged[key] = value  # ✓ Agregar (sin sobrescribir)
        else:
            # Clave existe en ambos
            # Si son dicts anidados, recursivamente mergear
            if isinstance(value, dict):
                merged[key] = merge(value, merged[key])
            else:
                # ✓ PRESERVAR valor local (no sobrescribir)
                pass
    
    return merged
```

---

## Próximos Pasos

1. ✅ Instalar: `./scripts/install.sh`
2. ✅ Personalizar: `nano config/local_config.yaml`
3. ✅ Probar merge: `python3 config/merge_config.py`
4. ✅ Setup crontab: `crontab -e` (ver [scripts/README.md](scripts/README.md))
5. ✅ Verificar logs: `tail /tmp/trt_autoupdate.log`

---

**Más info:** Ver [config/README.md](config/README.md) y [scripts/README.md](scripts/README.md)
