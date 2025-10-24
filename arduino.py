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
Serial.println("Comando recebido: " + msg);

if (msg == "abrir") servoPorta.write(180);   // abrir
else if (msg == "fechar") servoPorta.write(0); // fechar
}

void setup() {
Serial.begin(115200);
servoPorta.attach(0); // D3
servoPorta.write(90);

WiFi.begin(ssid, password);
while (WiFi.status() != WL_CONNECTED) {
delay(500);
Serial.print(".");
}
Serial.println("\n✅ WiFi conectado!");
Serial.print("📡 IP: ");
Serial.println(WiFi.localIP());

client.setServer(mqtt_server, 1883);
client.setCallback(callback);
}

void reconnect() {
while (!client.connected()) {
Serial.print("Tentando conectar ao MQTT...");
if (client.connect("ESP8266_GLAU")) {
Serial.println("conectado!");
client.subscribe(topic);
} else {
Serial.print("falhou, rc=");
Serial.print(client.state());
Serial.println(" Tentando novamente em 5 segundos.");
delay(5000);
}
}
}

void loop() {
if (!client.connected()) reconnect();
client.loop();
}
