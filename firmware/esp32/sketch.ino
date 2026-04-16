/*
  TRT Protocol Firmware - ESP32
  Implementa el protocolo TRT para ESP32
  
  Pin Mapping (configurable):
  - LED: GPIO2
  - Relé: GPIO27
  - Ventilador PWM: GPIO25
  - Sensor Temperatura: GPIO34 (ADC)
  - Sensor Humedad: GPIO35 (ADC)
*/

#define LED_PIN 2
#define RELAY_PIN 27
#define FAN_PWM_PIN 25
#define TEMP_SENSOR_PIN 34
#define HUM_SENSOR_PIN 35

// PWM Configuration
#define PWM_CHANNEL 0
#define PWM_FREQUENCY 5000
#define PWM_RESOLUTION 8

String incomingData = "";

void setup() {
  Serial.begin(115200);  // ESP32 típicamente usa 115200
  delay(2000);
  
  // Configurar pines
  pinMode(LED_PIN, OUTPUT);
  pinMode(RELAY_PIN, OUTPUT);
  
  // Configurar PWM para ventilador
  ledcSetup(PWM_CHANNEL, PWM_FREQUENCY, PWM_RESOLUTION);
  ledcAttachPin(FAN_PWM_PIN, PWM_CHANNEL);
  
  // Inicializar en LOW
  digitalWrite(LED_PIN, LOW);
  digitalWrite(RELAY_PIN, LOW);
  ledcWrite(PWM_CHANNEL, 0);
  
  Serial.println("READY");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();
    incomingData += c;
    
    if (c == '\n') {
      processCommand(incomingData);
      incomingData = "";
    }
  }
}

void processCommand(String cmd) {
  cmd.trim();
  cmd.toUpperCase();
  
  // Comandos digitales (LED, Relé)
  if (cmd == "LED_ON") {
    digitalWrite(LED_PIN, HIGH);
    Serial.println("OK");
  }
  else if (cmd == "LED_OFF") {
    digitalWrite(LED_PIN, LOW);
    Serial.println("OK");
  }
  else if (cmd == "RELAY_ON") {
    digitalWrite(RELAY_PIN, HIGH);
    Serial.println("OK");
  }
  else if (cmd == "RELAY_OFF") {
    digitalWrite(RELAY_PIN, LOW);
    Serial.println("OK");
  }
  
  // Comandos PWM (Ventilador)
  else if (cmd.startsWith("SET:FAN:")) {
    int pwmValue = cmd.substring(8).toInt();
    if (pwmValue < 0) pwmValue = 0;
    if (pwmValue > 255) pwmValue = 255;
    
    ledcWrite(PWM_CHANNEL, pwmValue);
    Serial.println("OK");
  }
  
  // Escritura general de pines
  else if (cmd.startsWith("WRITE_PIN:")) {
    int firstColon = cmd.indexOf(':');
    int secondColon = cmd.indexOf(':', firstColon + 1);
    
    int pin = cmd.substring(firstColon + 1, secondColon).toInt();
    int value = cmd.substring(secondColon + 1).toInt();
    
    analogWrite(pin, value);
    Serial.println("OK");
  }
  
  // Lectura de sensores
  else if (cmd.startsWith("SENSOR_READ:")) {
    int sensorNum = cmd.substring(12).toInt();
    int value;
    
    if (sensorNum == 0) {
      value = analogRead(TEMP_SENSOR_PIN);
    }
    else if (sensorNum == 1) {
      value = analogRead(HUM_SENSOR_PIN);
    }
    else {
      Serial.println("ERROR");
      return;
    }
    
    Serial.println(value);
  }
  
  // Comandos de información
  else if (cmd == "INFO") {
    Serial.println("BOARD:ESP32");
  }
  else if (cmd == "PING") {
    Serial.println("PONG");
  }
  
  else {
    Serial.println("ERROR");
  }
}
