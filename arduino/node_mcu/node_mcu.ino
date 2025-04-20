#include <Wire.h>
#include <ESP8266WiFi.h>
#include <WiFiClient.h>
#include <MPU6050.h>

const char* ssid = "SUA_REDE_WIFI";
const char* password = "SUA_SENHA_WIFI";

const char* host = "192.168.1.1";
const int port = 3000;
const char* path = "/monitor/";

MPU6050 mpu;
WiFiClient client;

void setup() {
  Serial.begin(115200);
  Wire.begin();

  mpu.initialize();
  if (!mpu.testConnection()) {
    Serial.println("MPU6050 não conectado!");
    while (1);
  }

  WiFi.begin(ssid, password);
  Serial.print("Conectando ao WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi conectado!");
}

void loop() {
  int16_t ax, ay, az;
  mpu.getAcceleration(&ax, &ay, &az);

  // Calcular o ângulo no eixo X (pitch)
  float angleX = atan2(ay, sqrt(ax * ax + az * az)) * 180.0 / PI;

  Serial.print("Ângulo X: ");
  Serial.println(angleX);

  int position = 0;

  // Margem de erro de ±5 graus
  if (angleX > 85 && angleX < 95) {
    position = 1;
  } else if (angleX > 175 || angleX < -175) {
    position = 2;
  }

  if (position > 0) {
    if (client.connect(host, port)) {
      String body = "position=" + String(position);
      String request =
        "POST " + String(path) + " HTTP/1.1\r\n" +
        "Host: " + host + "\r\n" +
        "Content-Type: application/x-www-form-urlencoded\r\n" +
        "Content-Length: " + body.length() + "\r\n" +
        "\r\n" +
        body;

      client.print(request);
      Serial.println("Requisição enviada:");
      Serial.println(body);

      // Esperar resposta
      while (client.connected()) {
        if (client.available()) {
          String line = client.readStringUntil('\n');
          Serial.println(line);
        }
      }
      client.stop();
    } else {
      Serial.println("Erro ao conectar ao servidor.");
    }

    delay(3000); // Evita múltiplas requisições seguidas
  }

  delay(500); // Pequeno delay para leitura mais estável
}
