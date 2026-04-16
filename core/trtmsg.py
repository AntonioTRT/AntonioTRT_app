import serial
import yaml
import os
import sys
import time

__version__ = "1.0.0"

class TRTMessage:
    def __init__(self):
        self.config = self._load_config()
        self.port = self.config.get('serial_port', '/dev/ttyUSB0')
        self.baudrate = self.config.get('baudrate', 9600)

    def _load_config(self):
        """Busca y carga el archivo local_config.yaml."""
        # Intenta encontrar el archivo en la carpeta config subiendo un nivel desde core/
        base_path = os.path.dirname(os.path.abspath(__file__))
        config_path = os.path.join(base_path, '../config/local_config.yaml')
        
        if not os.path.exists(config_path):
            # Si no existe el local, intenta cargar el default por seguridad
            config_path = os.path.join(base_path, '../config/default_config.yaml')
            
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except Exception as e:
            print(f"Error critico: No se pudo cargar la configuracion: {e}")
            sys.exit(1)

    def _handle_system_command(self, comando):
        """Maneja comandos internos del sistema (no requieren hardware)."""
        if comando == "version":
            return True, __version__
        elif comando == "help":
            help_text = """
Comandos del sistema TRT:
  version              - Muestra version de trtmsg
  help                 - Muestra esta ayuda

Comandos de hardware:
  send <modulo> <valor>  - Envía comando al microcontrolador
  ejemplo: python3 trtmsg.py send LED_ON 1
"""
            return True, help_text.strip()
        return False, f"Comando desconocido: {comando}"

    def send(self, modulo, valor):
        """Formatea y envia el mensaje al microcontrolador."""
        trama = f"{modulo}:{valor}\n"
        
        try:
            # Configuracion del puerto para evitar el auto-reset
            ser = serial.Serial()
            ser.port = self.port
            ser.baudrate = self.baudrate
            ser.timeout = 1
            ser.dtr = False  # Desactiva señal de reset
            ser.rts = False
            
            ser.open()
            
            # Pequeña pausa para estabilidad de la linea
            time.sleep(0.1)
            
            # Envio de datos
            ser.write(trama.encode('utf-8'))
            
            # Si el comando es de lectura (opcional), espera respuesta
            respuesta = None
            if modulo.startswith("get") or modulo.startswith("read"):
                respuesta = ser.readline().decode('utf-8').strip()
            
            ser.close()
            return True, respuesta if respuesta else "Comando enviado"

        except serial.SerialException as e:
            return False, f"Error de conexion serie: {e}"
        except Exception as e:
            return False, f"Error inesperado: {e}"

# Logica para ejecucion directa desde terminal (CLI)
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python3 trtmsg.py <comando> [valor]")
        print("Ejemplos:")
        print("  python3 trtmsg.py version")
        print("  python3 trtmsg.py help")
        print("  python3 trtmsg.py send LED_ON 1")
        sys.exit(1)

    comando_arg = sys.argv[1]
    
    # Comandos del sistema que no necesitan hardware
    if comando_arg == "version":
        print(__version__)
        sys.exit(0)
    elif comando_arg == "help":
        help_text = """
Comandos del sistema TRT:
  version              - Muestra version de trtmsg
  help                 - Muestra esta ayuda

Comandos de hardware:
  send <modulo> <valor>  - Envía comando al microcontrolador
  ejemplo: python3 trtmsg.py send LED_ON 1
"""
        print(help_text.strip())
        sys.exit(0)
    
    # Resto de comandos requieren hardware (inicializar messenger)
    messenger = TRTMessage()
    
    if len(sys.argv) < 3:
        print("Uso para comando de hardware: python3 trtmsg.py <modulo> <valor>")
        sys.exit(1)
    
    modulo_arg = sys.argv[1]
    valor_arg = " ".join(sys.argv[2:])
    
    exito, mensaje = messenger.send(modulo_arg, valor_arg)
    print(mensaje)
    
    # Exit con código de error si falló
    if not exito:
        sys.exit(1)