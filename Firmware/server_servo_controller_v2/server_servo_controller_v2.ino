#include "IK.h"
#include "actuator.h"
#include "leg.h"
#include <WiFi.h>
#include <cmath>
#include <iomanip>

//Adafruit_PWMServoDriver driver = Adafruit_PWMServoDriver();

int angleToPulse(int angle) {
  return map(angle, 0, 180, 100, 600);
}



const char* ssid     = "UPCD736725";
const char* password = "Y6Zcwbtruurb";
IPAddress local_IP(10, 0, 0, 1);
IPAddress gateway(10, 0, 0, 1);
IPAddress subnet(255, 255, 0, 0);
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8 , 4, 4); //optional
WiFiServer server(80);



int x, y, z = 0;
int stepTiming = 0;

int maxTime = 200;
int minTime = 50;

void up(Leg &leg) {
  leg.moveLeg(0, 50, 40);
}

void down(Leg & leg){
  leg.moveLeg(0, 50, 60);
}

void frontUp(Leg & leg) {
  leg.moveLeg(10, 50, 40);
}

void frontDown(Leg & leg) {
  leg.moveLeg(10, 50, 50);
}

void backDown(Leg & leg) {
  leg.moveLeg(-10, 50, 50);
}

void backUp(Leg & leg){
  leg.moveLeg(-10, 50, 40);
}


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
  Serial.print("Connecting to ");
  Serial.println(ssid);
  
  //  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
  //    Serial.println("Static settings failure");
  //  }
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(400);
    Serial.print(".");
    
  }

  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  
  server.begin();
  Actuator *jnt1 = new Actuator(0, 10, 60);
  Actuator *j2 = new Actuator(1, 0, 120);
  Actuator *j3 = new Actuator(2, 10, 80);

  Actuator *j4 = new Actuator(4, 100, 60);
  Actuator *j5 = new Actuator(5, 100, 120);
  Actuator *j6 = new Actuator(6, 100, 60);

  Actuator *j7 = new Actuator(7, 100, 60);
  Actuator *j8 = new Actuator(8, 100, 120);
  Actuator *j9 = new Actuator(9, 100, 60);

  Actuator *j10 = new Actuator(10, 100, 60);
  Actuator *j11 = new Actuator(11, 100, 120);
  Actuator *jnt12 = new Actuator(12, 100, 60);

  Leg* leg_1 = new Leg(1, "front_right", *jnt1, *j2, *j3);
  Leg* leg_2 = new Leg(2, "back_right", *j4, *j5, * j6 );
  Leg* leg_3 = new Leg(3, "front_left", *j7, *j8, *j9 );
  Leg* leg_4 = new Leg(4, "back_right", *j10, *j11, *jnt12 );
  Serial.println(leg_1->getStats());
  up(*leg_1);

  
  
  while (1) {
    WiFiClient client = server.available();   // listen for incoming clients

    if (client) {
      while ( client.connected() ) {
        int     byteSize = 0;
        uint8_t dataPacket[256];
        if (byteSize = client.available()) {
          for (int i = 0; i < byteSize; i++) {
            dataPacket[i] = client.read();
            Serial.print(dataPacket[i]);
          }

          Serial.println();
          if(dataPacket[0] == 11){
            if (stepTiming >= maxTime){
              Serial.println("Max Step size reached");
            }
            else {
              stepTiming += 5;
            }
            Serial.println("Step Time: " + String(stepTiming));
          }

          else if(dataPacket[0] == 12) {
            
            if(stepTiming <= minTime){
              Serial.println("Min step size reached");
            }
            else {
              stepTiming -= 5;
            }
            Serial.println("Step Time: " + String(stepTiming));
          }
          
          else if(dataPacket[0] == 10) {
            frontUp(*leg_1);
            delay(stepTiming);
            frontDown(*leg_1);
            delay(stepTiming);
            backDown(*leg_1);
            delay(stepTiming);
            backUp(*leg_1);
            delay(stepTiming);
          }
          else if(dataPacket[0] == 1){
            x += 5;
            leg_1->moveLeg(x, y, z);
          }
          else if (dataPacket[0] == 2) {
            x -= 5;
            leg_1->moveLeg(x, y, z);
          }
          else if (dataPacket[0] == 3) {
            y += 5;
            leg_1->moveLeg(x, y, z);
          }
          else if (dataPacket[0] == 4) {
            y -= 5;
            leg_1->moveLeg(x, y, z);
          }
          else if (dataPacket[0] == 5) {
            z += 5;
            leg_1->moveLeg(x, y, z);
          }
          else if(dataPacket[0] == 6) {
            z -= 5;
            leg_1->moveLeg(x, y, z);
          }

          //leg_1->moveLeg(dataPacket[0], dataPacket[1], dataPacket[2]);

          Serial.println("X: " + String(x) + " Y: " + String(y) + " Z: " + String(z));
          Serial.println();
          client.stop();
        }
      }
    }
    delay(5);
  }
}





void loop() {


}
