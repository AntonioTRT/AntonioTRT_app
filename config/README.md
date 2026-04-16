# 📋 Configuración - TRT App

Esta carpeta contiene los archivos de configuración YAML para TRT-AntonioTRT_app.

## Tipos de Configuración

### `default_config.yaml`
Configuración por defecto para todas las Raspberry Pi. **Se commitea a git.**

Contiene todos los campos estándar que la aplicación necesita.

### `local_config.yaml`
Configuración local **específica de cada Raspberry Pi**. **NO se commitea a git** (está en `.gitignore`).

Permite que cada dispositivo tenga su propia configuración sin afectar el repositorio compartido.

### `merge_config.py`
Script inteligente que sincroniza `default_config.yaml` con `local_config.yaml`.

**Garantiza que:**
- ✅ Primera instalación: copia default → local
- ✅ Actualizaciones posteriores: **preserva todos los valores locales**
- ✅ Nuevas variables: **se agregan automáticamente** sin perder datos
- ✅ Variables eliminadas: se mantienen (es reversible)

---

## Flujo Automático de Configuración

```
PRIMERA INSTALACIÓN (git clone + ./scripts/install.sh)
↓
merge_config.py se ejecuta
↓
¿Existe local_config.yaml?
├─ NO:  copia default_config.yaml → local_config.yaml
└─ SÍ:  merge inteligente (preserva valores locales)
↓
Aplicación usa local_config.yaml


ACTUALIZACIÓN POSTERIOR (git pull + autoupdate.sh)
↓
git pull --recurse-submodules
↓
merge_config.py se ejecuta automáticamente
↓
default_config.yaml cambió?
├─ NUEVAS CLAVES: se agregan a local_config.yaml
├─ CLAVES EXISTENTES: se respetan valores locales
└─ CLAVES ELIMINADAS: se conservan en local (reversible)
↓
Aplicación sigue usando los valores locales personalizados
```

---

## Cómo Funciona el Merge

### Ejemplo 1: Primera Instalación

```yaml
# default_config.yaml (remoto)
pi_name: RaspberryPi-B
board_type: uno
serial_port: /dev/ttyUSB0
baudrate: 9600
features:
  has_lcd: false
  has_fan: false

# Después de primera instalación:
# local_config.yaml (copia idéntica de default)
```

### Ejemplo 2: Actualización con Nueva Variable

```yaml
# default_config.yaml (actualizado en remoto)
pi_name: RaspberryPi-B
board_type: uno
serial_port: /dev/ttyUSB0
baudrate: 9600
debug_mode: false              # ← NUEVA VARIABLE
features:
  has_lcd: false
  has_fan: false
  has_relay: true              # ← NUEVA CARACTERÍSTICA

# local_config.yaml (personalizado localmente)
pi_name: "Mi-Raspberry-Cocina"     # ← RESPETADO (no se sobrescribe)
board_type: uno
serial_port: /dev/ttyACM0          # ← RESPETADO (puerto diferente)
baudrate: 115200                   # ← RESPETADO (baudrate personalizado)
features:
  has_lcd: true
  has_fan: true

# Después de merge automático:
pi_name: "Mi-Raspberry-Cocina"     # ✓ Preservado
board_type: uno
serial_port: /dev/ttyACM0          # ✓ Preservado
baudrate: 115200                   # ✓ Preservado
debug_mode: false                  # ✓ Nueva, agregada
features:
  has_lcd: true                    # ✓ Preservado
  has_fan: true                    # ✓ Preservado
  has_relay: true                  # ✓ Nuevo, agregado
```

---

## Uso Manual

Si necesitas sincronizar manualmente (sin esperar a `autoupdate.sh`):

```bash
# Sincronizar configuración
python3 config/merge_config.py

# Modo silencioso (menos output)
python3 config/merge_config.py --quiet

# Dry-run (simular cambios sin guardar) [próximamente]
python3 config/merge_config.py --dry-run
```

---

## Cómo Configurar por Primera Vez

### 1. Instalación Inicial

```bash
# Clonar con submodules
git clone --recurse-submodules https://github.com/usuario/TRT-AntonioTRT_app.git
cd TRT-AntonioTRT_app

# Instalación automática (ejecuta merge_config.py)
chmod +x scripts/*.sh
./scripts/install.sh
```

El script `install.sh` automáticamente:
1. Ejecuta `config/merge_config.py`
2. Crea `local_config.yaml` (si no existe)

### 2. Personalizar Configuración

```bash
# Editar valores locales
nano config/local_config.yaml
```

Campos a personalizar:
```yaml
pi_name: "RaspberryPi-5-Salon"     # Nombre único para esta Pi
board_type: "uno"                   # 'uno' o 'esp32'
serial_port: "/dev/ttyUSB0"        # Puerto (ls /dev/tty* para listar)
baudrate: 9600                      # Velocidad (9600, 115200, etc)
features:
  has_lcd: true                     # ¿Tiene display?
  has_fan: true                     # ¿Tiene ventilador?
```

### 3. Verificar Configuración

```bash
# Ver valores que se cargarán
cat config/local_config.yaml

# Verificar que la app los lee correctamente
python3 -c "from core import get_trt_handler; h = get_trt_handler(); print(h.get_board_info())"
```

---

## Detección de Puerto Serial

Si no sabes qué puerto usar:

**Raspberry Pi / Linux:**
```bash
ls /dev/tty*
# Busca: /dev/ttyUSB0, /dev/ttyACM0, etc
```

**Windows (PowerShell):**
```powershell
Get-SerialPort
# O: mode
```

**Verificar en Arduino IDE:**
- Tools → Port → te muestra el puerto actual

---

## Actualizaciones Automáticas (Crontab)

Cuando configures `autoupdate.sh` en crontab, **automáticamente**:
1. Ejecuta `git pull --recurse-submodules`
2. Ejecuta `config/merge_config.py` (preserva local_config.yaml)
3. Actualiza dependencias si requirements cambió
4. Flashea firmware si cambió
5. Reinicia el servicio

**Instalación en crontab:**
```bash
# Editar
crontab -e

# Agregar línea (cada 10 minutos):
*/10 * * * * /home/pi/TRT-AntonioTRT_app/scripts/autoupdate.sh >> /tmp/trt_autoupdate.log 2>&1
```

Ver lógica completa en [scripts/README.md](../scripts/README.md)

---

## ⚠️ Casos Especiales

### Caso 1: Revertir a Default

Si quieres descartar cambios locales y volver a default:

```bash
# Respaldar (por si acaso)
cp config/local_config.yaml config/local_config.yaml.backup

# Copiar default
cp config/default_config.yaml config/local_config.yaml

# Ejecutar merge (opcional, ya que es idéntico)
python3 config/merge_config.py
```

### Caso 2: Sincronizar Múltiples Raspberries

Si tienes varias Pis con diferente hardware:

**Raspberry Pi B (port /dev/ttyUSB0):**
```yaml
pi_name: "RaspberryPi-B-Garage"
serial_port: "/dev/ttyUSB0"
board_type: "uno"
```

**Raspberry Pi 5 (port /dev/ttyACM0):**
```yaml
pi_name: "RaspberryPi-5-Kitchen"
serial_port: "/dev/ttyACM0"
board_type: "esp32"
baudrate: 115200
```

Cada una mantiene su propia `local_config.yaml` automáticamente.

### Caso 3: Agregar Nueva Variable al Default

Si necesitas agregar un nuevo campo a `default_config.yaml`:

```yaml
# default_config.yaml
pi_name: RaspberryPi-B
board_type: uno
serial_port: /dev/ttyUSB0
baudrate: 9600
new_feature: true              # ← Nueva variable
```

**Luego:**
1. Haz commit y push a GitHub
2. Cuando corra `autoupdate.sh` en una Pi, automáticamente:
   - Descargará el cambio
   - Ejecutará `merge_config.py`
   - Agregará `new_feature: true` a su `local_config.yaml`

---

## Troubleshooting

### "local_config.yaml no se sincroniza"

```bash
# Ejecutar manualmente
python3 config/merge_config.py

# Si no funciona, verificar permisos
ls -la config/
chmod 644 config/*.yaml
```

### "Perdí valores personalizados"

```bash
# Si tienes backup
cp config/local_config.yaml.backup config/local_config.yaml

# Si no, recrear desde default y re-personalizar
cp config/default_config.yaml config/local_config.yaml
nano config/local_config.yaml  # Volver a poner tus valores
```

### "Variables antiguas aún aparecen"

Es intencional. El merge preserva variables antiguas para rever reversibilidad. Si quieres limpiar:

```bash
# Crear nuevo desde default
cp config/default_config.yaml config/local_config.yaml

# Re-personalizar
nano config/local_config.yaml
```

---

## Notas Importantes

✓ **`local_config.yaml` NUNCA se commitea** - Git la ignora  
✓ **`default_config.yaml` SIEMPRE se commitea** - Es el reference
✓ **El merge es unidireccional** - Default → Local (nunca Local → Default)  
✓ **Es reversible** - Puedes restaurar default en cualquier momento  
✓ **Variables nuevas se agregan automáticamente** - Sin perder datos  

---

Para más información sobre las opciones de configuración disponibles, ver [README raíz](../README.md)

