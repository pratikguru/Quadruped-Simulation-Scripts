#include "IK.h"
#include "actuator.h"
#include "leg.h"



void setup() {
  // put your setup code here, to run once:

    Serial.begin(115200);
    
    Actuator* j1 = new Actuator(1, 100, 60);
    Actuator* j2 = new Actuator(2, 100, 120);
    Actuator* j3 = new Actuator(3, 100, 60);

    Actuator* j4 = new Actuator(4, 100, 60);
    Actuator* j5 = new Actuator(5, 100, 120);
    Actuator* j6 = new Actuator(6, 100, 60);

    Actuator* j7 = new Actuator(7, 100, 60);
    Actuator* j8 = new Actuator(8, 100, 120);
    Actuator* j9 = new Actuator(9, 100, 60);

    Actuator* j10 = new Actuator(10, 100, 60);
    Actuator* j11 = new Actuator(11, 100, 120);
    Actuator* j12 = new Actuator(12, 100, 60);
    

    Leg* leg_1 = new Leg(1, "front_right", *j1, *j2, *j3);
    Leg* leg_2 = new Leg(2, "back_right", *j4, *j5, *j6);
    Leg* leg_3 = new Leg(3, "front_left", *j7, *j8, *j9);
    Leg* leg_4 = new Leg(4, "back_right", *j10, *j11, *j12);

    Serial.println(leg_1->getStats());
    Serial.println(leg_2->getStats());
    Serial.println(leg_3->getStats());
    Serial.println(leg_3->getStats());


    leg_1->actuateLeg(20,20,20);
    for(int i = 0; i < 10; i++) {
       leg_1->moveLeg(0, i, 130);
    }
    
}

void loop() {
  // put your main code here, to run repeatedly:

}
