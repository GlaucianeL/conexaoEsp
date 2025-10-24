#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>

const char* ssid = "I4";
const char* password = "I4emssocara@nov2023";
const char* mqtt_server = "broker.hivemq.com";

WiFiClient espClient;
PubSubClient client(espClient);
Servo servoPorta;

const char* topic = "glaucia/porta";

void callback(char* topic, byte* payload, unsigned int length) {
  String msg;
  for (int i = 0; i < length; i++) msg += (char)payload[i];
  Serial.println("Comando: " + msg);

  if (msg == "open") servoPorta.write(180);
  else if (msg == "close") servoPorta.write(0);
}

void setup() {
  Serial.begin(115200);
  servoPorta.attach(0); // D3
  servoPorta.write(90);

  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) { delay(500); Serial.print("."); }
  Serial.println("WiFi conectado");

  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}

void reconnect() {
  while (!client.connected()) {
    if (client.connect("ESP8266_GLAU")) {
      client.subscribe(topic);
    } else {
      delay(5000);
    }
  }
}

void loop() {
  if (!client.connected()) reconnect();
  client.loop();
}
