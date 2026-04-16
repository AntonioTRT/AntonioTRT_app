#ifndef CONFIG_H
#define CONFIG_H

// Configuracion de la LCD
#define LCD_ADDR 0x3F    // Direccion I2C (0x27 o 0x3F)
#define LCD_COLS 16      // Columnas de la LCD
#define LCD_ROWS 2       // Filas de la LCD

// Definicion de Pines
#define FAN_PIN 3        // Pin PWM para el ventilador

// Parametros de comunicacion
#define SERIAL_BAUD 9600 // Velocidad del puerto serie

#endif