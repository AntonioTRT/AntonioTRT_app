import serial
import serial.tools.list_ports
import yaml
import os
import sys
import time

__version__ = "1.0.0"

class TRTMessage:
    def __init__(self, port=None, baudrate=None):
        self.config = self._load_config()
        self.port = port if port else self.config.get('serial_port', '/dev/ttyUSB0')
        self.baudrate = baudrate if baudrate else self.config.get('baudrate', 9600)

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

    @staticmethod
    def list_devices(show_all=False):
        """Lista los puertos COM disponibles en el sistema."""
        ports = []
        
        # Usar pyserial para detectar puertos
        available_ports = serial.tools.list_ports.comports()
        
        if not available_ports:
            return "No se encontraron puertos COM disponibles."
        
        output = "\nPuertos COM disponibles:\n"
        output += "-" * 60 + "\n"
        
        for port in available_ports:
            port_info = f"Puerto: {port.device}"
            if show_all:
                port_info += f"\n  Descripcion: {port.description}"
                port_info += f"\n  Hardware: {port.hwid}"
            output += port_info + "\n"
        
        output += "-" * 60
        return output

    def lcd_set_message(self, mensaje):
        """Envía un mensaje a la pantalla LCD."""
        # Limitar a 32 caracteres (2 líneas de 16 caracteres)
        if len(mensaje) > 32:
            mensaje = mensaje[:32]
        
        # Formato corregido para coincidir con Arduino: lcd:mensaje
        trama = f"lcd:{mensaje}\n"
        
        try:
            ser = serial.Serial()
            ser.port = self.port
            ser.baudrate = self.baudrate
            ser.timeout = 1
            ser.dtr = False
            ser.rts = False
            
            ser.open()
            time.sleep(0.1)
            
            ser.write(trama.encode('utf-8'))
            
            # Leer respuesta
            respuesta = ser.readline().decode('utf-8').strip()
            ser.close()
            
            return True, respuesta if respuesta else "Mensaje enviado al LCD"
        
        except serial.SerialException as e:
            return False, f"Error de conexion: {e}"
        except Exception as e:
            return False, f"Error: {e}"


class TRTMessageHandler(TRTMessage):
    """Alias compatible con la API de pruebas y la UI."""
    pass

_trt_handler_instance = None

def get_trt_handler():
    global _trt_handler_instance
    if _trt_handler_instance is None:
        _trt_handler_instance = TRTMessageHandler()
    return _trt_handler_instance

# Logica para ejecucion directa desde terminal (CLI)
if __name__ == "__main__":
    def extract_port(args):
        if '-u' in args:
            idx = args.index('-u')
            if idx + 1 < len(args):
                port = args[idx + 1]
                del args[idx:idx + 2]
                return port
        return None

    if len(sys.argv) < 2:
        print("Uso: python3 trtmsg.py <comando> [valor]")
        print("Ejemplos:")
        print("  python3 trtmsg.py version")
        print("  python3 trtmsg.py help")
        print("  python3 trtmsg.py send LED_ON 1 -u COM3")
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
  devices [-a]         - Lista puertos COM disponibles
  help                 - Muestra esta ayuda

Comandos de hardware:
  send <modulo> <valor> [-u <puerto>]      - Envía comando al microcontrolador
  lcd set "mensaje" [-u <puerto>]         - Envía mensaje a pantalla LCD
  analogread <pin> [-u <puerto>]          - Lee valor analógico del pin (1-5)
  digitalwrite <pin> <estado> [-u <puerto>] - Controla pin digital (2-13, 0/1)
  readlcd [-u <puerto>]                   - Lee mensaje actual de la LCD
  reboot [-u <puerto>]                    - Reinicia el Arduino

Ejemplos:
  trtmsg version
  trtmsg devices -a
  trtmsg send LED_ON 1 -u COM3
  trtmsg lcd set "Hola Mundo" -u /dev/ttyUSB0
  trtmsg analogread 3 -u COM3
  trtmsg digitalwrite 5 1 -u COM3
  trtmsg readlcd -u COM3
  trtmsg reboot -u COM3
"""
        print(help_text.strip())
        sys.exit(0)
    elif comando_arg == "devices":
        show_all = "-a" in sys.argv or "--all" in sys.argv
        resultado = TRTMessage.list_devices(show_all=show_all)
        print(resultado)
        sys.exit(0)
    elif comando_arg == "lcd":
        port = extract_port(sys.argv)
        if len(sys.argv) < 4:
            print("Uso: trtmsg lcd set \"mensaje\" -u <puerto>")
            sys.exit(1)
        
        subcomando = sys.argv[2]
        
        if subcomando == "set":
            mensaje = " ".join(sys.argv[3:])
            messenger = TRTMessage(port=port)
            exito, resultado = messenger.lcd_set_message(mensaje)
            print(resultado)
            sys.exit(0 if exito else 1)
        else:
            print("Subcomando desconocido. Usa: trtmsg lcd set \"mensaje\" -u <puerto>")
            sys.exit(1)
    elif comando_arg == "analogread":
        port = extract_port(sys.argv)
        if len(sys.argv) < 3:
            print("Uso: trtmsg analogread <pin> -u <puerto>")
            sys.exit(1)
        
        pin = sys.argv[2]
        messenger = TRTMessage(port=port)
        exito, resultado = messenger.send("analogread", pin)
        print(resultado)
        sys.exit(0 if exito else 1)
    elif comando_arg == "digitalwrite":
        port = extract_port(sys.argv)
        if len(sys.argv) < 4:
            print("Uso: trtmsg digitalwrite <pin> <estado> -u <puerto>")
            sys.exit(1)
        
        pin = sys.argv[2]
        estado = sys.argv[3]
        valor = f"{pin}:{estado}"
        messenger = TRTMessage(port=port)
        exito, resultado = messenger.send("digitalwrite", valor)
        print(resultado)
        sys.exit(0 if exito else 1)
    elif comando_arg == "readlcd":
        port = extract_port(sys.argv)
        messenger = TRTMessage(port=port)
        exito, resultado = messenger.send("readlcd", "")
        print(resultado)
        sys.exit(0 if exito else 1)
    elif comando_arg == "reboot":
        port = extract_port(sys.argv)
        messenger = TRTMessage(port=port)
        exito, resultado = messenger.send("reboot", "")
        print(resultado)
        sys.exit(0 if exito else 1)
    
    # Resto de comandos requieren hardware (inicializar messenger)
    port = extract_port(sys.argv)
    messenger = TRTMessage(port=port)
    
    if len(sys.argv) < 3:
        print("Uso para comando de hardware: python3 trtmsg.py <modulo> <valor> -u <puerto>")
        sys.exit(1)
    
    modulo_arg = sys.argv[1]
    valor_arg = " ".join(sys.argv[2:])
    
    exito, mensaje = messenger.send(modulo_arg, valor_arg)
    print(mensaje)
    
    # Exit con código de error si falló
    if not exito:
        sys.exit(1)