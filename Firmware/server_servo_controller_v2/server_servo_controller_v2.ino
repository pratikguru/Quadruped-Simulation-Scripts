#include "IK.h"
#include "actuator.h"
#include "leg.h"
#include <WiFi.h>
#include <cmath>
#include <iomanip>

#define RUN_ROBOT_ON_SERVER       true
#define STATIC_SERVER_CREDENTIALS false

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
int legCount = 1;

int maxTime = 200;
int minTime = 50;

void up(Leg &leg) {
  leg.moveLeg(0, 60, 40);
}

void down(Leg & leg) {
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

void backUp(Leg & leg) {
  leg.moveLeg(-10, 50, 40);
}


void setup() {
  // put your setup code here, to run once:

  Serial.begin(115200);
#if RUN_ROBOT_ON_SERVER
  Serial.print("Connecting to ");
  Serial.println(ssid);

#if STATIC_SERVER_CREDENTIALS
  Serial.println("Setting Static Server Credentials");
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
    Serial.println("Static settings failure");
  }
#endif

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
#else
  Serial.println("No Server Running");
#endif


  Actuator *jnt1 = new Actuator(0, 0, 60);
  Actuator *j2 = new Actuator(1, 0, 120);
  Actuator *j3 = new Actuator(2, 0, 80);

  Actuator *j4 = new Actuator(4, 0, 60);
  Actuator *j5 = new Actuator(5, 0, 120);
  Actuator *j6 = new Actuator(6, 0, 60);

  Actuator *j7 = new Actuator(8, 10, 60);
  Actuator *j8 = new Actuator(9, 0, 120);
  Actuator *j9 = new Actuator(10, 0, 60);

  Actuator *j10 = new Actuator(12, 10, 60);
  Actuator *j11 = new Actuator(13, 12, 120);
  Actuator *jnt12 = new Actuator(15, 0, 60);

  Leg* leg_1 = new Leg(1, "front_right", *jnt1, *j2,  *j3);
  Leg* leg_2 = new Leg(2, "back_right",  *j4,   *j5,  *j6 );
  Leg* leg_3 = new Leg(3, "front_left",  *j7,   *j8,  *j9 );
  Leg* leg_4 = new Leg(4, "back_right",  *j10,  *j11, *jnt12 );

  Serial.println(leg_1->getStats());
  Serial.println(leg_2->getStats());
  Serial.println(leg_3->getStats());
  Serial.println(leg_4->getStats());


  up(*leg_1);
  up(*leg_2);
  up(*leg_3);
  up(*leg_4);
  delay(500);
  down(*leg_1);
  down(*leg_2);
  down(*leg_3);
  down(*leg_4);
  delay(500);

  //  down(*leg_1);
  //  down(*leg_2);
  //  down(*leg_3);
  //  down(*leg_4);
  ////
  //  for(int i = 0; i < 5; i++) {
  //    leg_1->actuateLeg(90, 0, 90);
  //    leg_2->actuateLeg(90, 0, 90);
  //    leg_3->actuateLeg(90, 0, 90);
  //    leg_4->actuateLeg(90, 0, 90);
  //    delay(500);
  //    leg_1->actuateLeg(90, 90, 0);
  //    leg_2->actuateLeg(90, 90, 0);
  //    leg_3->actuateLeg(90, 90, 0);
  //    leg_4->actuateLeg(90, 90, 0);
  //    delay(500);
  //  }


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


          if (dataPacket[0] == 11) {
            if (stepTiming >= maxTime) {
              Serial.println("Max Step size reached");
            }
            else {
              stepTiming += 5;
            }
            Serial.println("Step Time: " + String(stepTiming));
          }

          else if (dataPacket[0] == 12) {

            if (stepTiming <= minTime) {
              Serial.println("Min step size reached");
            }
            else {
              stepTiming -= 5;
            }
            Serial.println("Step Time: " + String(stepTiming));
          }

          else if (dataPacket[0] == 13) {
            Serial.println("Resetting legs");
            x = 0;
            y = 50;
            z = 40;
            leg_1->moveLeg(x, y, z);
          }
          else if (dataPacket[0] == 20) {
            Serial.println("Incrementing Leg");
            if (legCount >= 4) {
              legCount = 1;
            }
            else {
              legCount += 1;
            }
            Serial.println("Leg: " + String (legCount));
          }
          else if (dataPacket[0] == 10) {
            //frontUp(*leg_1);
//            frontUp(*leg_2);
//            frontUp(*leg_3);
//            frontUp(*leg_4);
//            leg_2->moveLeg(10, 50, 40);
//            leg_3->moveLeg(10, 50, 40);
            leg_4->moveLeg(10, 50, 40);
            delay(stepTiming);
            //frontDown(*leg_1);
//            leg_2->moveLeg(10, 50, 50);
//            leg_3->moveLeg(10, 50, 50);
            leg_4->moveLeg(10, 50, 50);
//            frontDown(*leg_2);
//            frontDown(*leg_3);
//            frontDown(*leg_4);
            delay(stepTiming);
            //backDown(*leg_1);
//            leg_2->moveLeg(-10, 50, 50);
//            leg_3->moveLeg(-10, 50, 50);
            leg_4->moveLeg(-10, 50, 50);
//            backDown(*leg_2);
//            backDown(*leg_3);
//            backDown(*leg_4);
            delay(stepTiming);
            //backUp(*leg_1);
//            leg_2->moveLeg(-10, 50, 40);
//            leg_3->moveLeg(-10, 50, 40);
            leg_4->moveLeg(-10, 50, 40);
//            backUp(*leg_2);
//            backUp(*leg_3);
//            backUp(*leg_4);
            delay(stepTiming);
          }
          else if (dataPacket[0] == 1) {
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
          else if (dataPacket[0] == 6) {
            z -= 5;
            leg_1->moveLeg(x, y, z);
          }
          Serial.println("X: " + String(x) + " Y: " + String(y) + " Z: " + String(z));
          Serial.println();
          client.stop();
        }
      }
    }
    delay(3);
  }

}





void loop() {


}
