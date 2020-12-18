#include <iostream>
#include "leg.h"
#include "IK.h"
#include "actuator.h"


int main(){
    std::cout << "Ready!" << std::endl;

    Actuator* j1 = new Actuator(1, 100);
    Actuator* j2 = new Actuator(3, 100);
    Actuator* j3 = new Actuator(3, 100);

    Actuator* j4 = new Actuator(4, 100);
    Actuator* j5 = new Actuator(5, 100);
    Actuator* j6 = new Actuator(6, 100);

    Actuator* j7 = new Actuator(7, 100);
    Actuator* j8 = new Actuator(8, 100);
    Actuator* j9 = new Actuator(9, 100);

    Actuator* j10 = new Actuator(10, 100);
    Actuator* j11 = new Actuator(11, 100);
    Actuator* j12 = new Actuator(12, 100);
    

    Leg* leg_1 = new Leg(1, "front_right", *j1, *j2, *j3);
    Leg* leg_2 = new Leg(2, "back_right", *j4, *j5, *j6);
    Leg* leg_3 = new Leg(3, "front_left", *j7, *j8, *j9);
    Leg* leg_4 = new Leg(4, "back_right", *j10, *j11, *j12);
    std::cout << leg_1->getStats();
    std::cout << leg_2->getStats();
    std::cout << leg_3->getStats();
    std::cout << leg_4->getStats();

    leg_1->actuateLeg(90, 90, 90);
    return 0;
}