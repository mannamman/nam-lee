#include "EspMQTTClient.h"

const int stepPin[4] = {5,4,14,12};
int delay1 = 3;

EspMQTTClient client(
  "404",  // wifi name
  "47525804752580",  // wifi password
  "192.168.43.20",  // MQTT Broker server ip
  "MQTTUsername",   // Can be omitted if not needed
  "MQTTPassword",   // Can be omitted if not needed
  "TestClient"      // Client name that uniquely identify your device
);

void setup() {

  Serial.begin(115200);  

    for(int i=0; i<4; i++){
    pinMode(stepPin[i], OUTPUT);
  }

  for(int i=0; i<4; i++){
    digitalWrite(stepPin[i], LOW);
  }
}

void onConnectionEstablished() {

  client.subscribe("/order", [] (const String &payload)  {
    Serial.println(payload);
    if(payload == "1")
    {
      for(int i=0; i<43; i++){
        stepmoveF();
      }
    }
    if(payload == "-1")
    {
      for(int i=0; i<43; i++){
        stepmoveR();
      }
    }
  });
}

void loop() {
  client.loop();
}

void pinControl(int a, int b, int c, int d, int delayval){
  digitalWrite(stepPin[0],a);
  digitalWrite(stepPin[1],b);
  digitalWrite(stepPin[2],c);
  digitalWrite(stepPin[3],d);
  delay(delayval);
}

void stepmoveR(){
  pinControl(1,0,0,0,delay1);
  pinControl(1,1,0,0,delay1);
  pinControl(0,1,0,0,delay1);
  pinControl(0,1,1,0,delay1);
  pinControl(0,0,1,0,delay1);
  pinControl(0,0,1,1,delay1);
  pinControl(0,0,0,1,delay1);
  pinControl(1,0,0,1,delay1);
}

void stepmoveF(){
  pinControl(1,0,0,1,delay1);
  pinControl(0,0,0,1,delay1);
  pinControl(0,0,1,1,delay1);
  pinControl(0,0,1,0,delay1);
  pinControl(0,1,1,0,delay1);
  pinControl(0,1,0,0,delay1);
  pinControl(1,1,0,0,delay1);
  pinControl(1,0,0,0,delay1);
}