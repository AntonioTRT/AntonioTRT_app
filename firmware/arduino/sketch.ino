#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include "config.h"

// Inicializar LCD con los valores de config.h
LiquidCrystal_I2C lcd(LCD_ADDR, LCD_COLS, LCD_ROWS);

void setup() {
  // Iniciar comunicacion serie
  Serial.begin(SERIAL_BAUD);
  
  // Iniciar LCD
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0, 0);
  lcd.print("TRT Bridge Ready");
  
  // Configurar pin del ventilador usando la definicion de config.h
  pinMode(FAN_PIN, OUTPUT);
  analogWrite(FAN_PIN, 0); 
}

void loop() {
  if (Serial.available() > 0) {
    String data = Serial.readStringUntil('\n');
    data.trim();
    
    int separatorIndex = data.indexOf(':');
    
    if (separatorIndex != -1) {
      String modulo = data.substring(0, separatorIndex);
      String valor = data.substring(separatorIndex + 1);
      
      ejecutarComando(modulo, valor);
    }
  }
}

void ejecutarComando(String modulo, String valor) {
  if (modulo == "fan") {
    int potencia = valor.toInt();
    potencia = constrain(potencia, 0, 255);
    
    // Pulso de arranque para romper la inercia del motor
    if (potencia > 0 && potencia < 100) {
      analogWrite(FAN_PIN, 255);
      delay(50);
    }
    
    analogWrite(FAN_PIN, potencia);
  } 
  
  else if (modulo == "lcd") {
    lcd.clear();
    lcd.setCursor(0, 0);
    
    if (valor.length() <= LCD_COLS) {
      lcd.print(valor);
    } else {
      lcd.print(valor.substring(0, LCD_COLS));
      lcd.setCursor(0, 1);
      lcd.print(valor.substring(LCD_COLS, LCD_COLS * 2));
    }
  }
}