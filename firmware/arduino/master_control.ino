#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <avr/wdt.h> // Librería para el reinicio por software

LiquidCrystal_I2C lcd(0x27, 16, 2); 
String mensajeActual = "Status: READY";

// --- FUNCIONES PARA MANEJAR COMANDOS ---
void handleLCD(String val) {
  lcd.clear();         // Limpia restos de mensajes anteriores
  lcd.setCursor(0, 0);
  lcd.print(val);
  mensajeActual = val;
  Serial.println("ACK:LCD_UPDATED");
}

void handleReadLCD() {
  Serial.print("CURRENT_LCD:");
  Serial.println(mensajeActual);
}

void handleAnalogRead(int pin) {
  if (pin >= 1 && pin <= 5) {
    int lectura = analogRead(pin);
    Serial.print("PIN_A");
    Serial.print(pin);
    Serial.print("_VALUE:");
    Serial.println(lectura);
  } else {
    Serial.println("ERROR:INVALID_PIN_1-5");
  }
}

void handleDigitalWrite(int pin, int state) {
  if (pin >= 2 && pin <= 13) {  // Pines digitales seguros (evita 0/1 para serial)
    pinMode(pin, OUTPUT);
    digitalWrite(pin, state);
    Serial.print("ACK:DIGITAL_PIN_");
    Serial.print(pin);
    Serial.print("_SET_TO:");
    Serial.println(state);
  } else {
    Serial.println("ERROR:INVALID_PIN_2-13");
  }
}

void setup() {
  Serial.begin(9600);
  
  lcd.init();
  lcd.backlight();
  lcd.clear(); // Asegura pantalla limpia al iniciar
  lcd.setCursor(0, 0);
  lcd.print("TRT System");
  lcd.setCursor(0, 1);
  lcd.print(mensajeActual);

  Serial.println("SYSTEM:ONLINE");
}

void loop() {
  if (Serial.available() > 0) {
    String trama = Serial.readStringUntil('\n');
    trama.trim();

    int separador = trama.indexOf(':');
    String cmd, val;

    if (separador != -1) {
      cmd = trama.substring(0, separador);
      val = trama.substring(separador + 1);
    } else {
      cmd = trama; 
    }

    // --- LLAMADAS A FUNCIONES SEGÚN COMANDO ---
    if (cmd == "lcd") {
      handleLCD(val);
    }
    else if (cmd == "readlcd") {
      handleReadLCD();
    }
    else if (cmd == "analogread") {
      int pin = val.toInt();
      handleAnalogRead(pin);
    }
    else if (cmd == "digitalwrite") {
      int separador2 = val.indexOf(':');
      if (separador2 != -1) {
        int pin = val.substring(0, separador2).toInt();
        int state = val.substring(separador2 + 1).toInt();
        handleDigitalWrite(pin, state);
      } else {
        Serial.println("ERROR:INVALID_FORMAT_PIN:STATE");
      }
    }
    else if (cmd == "reboot") {
      handleReboot();
    }
    // Agregar más comandos aquí si es necesario
  }
}