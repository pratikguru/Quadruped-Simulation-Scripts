#ifndef LEG_H
#define LEG_H 
#include "actuator.h"
#include <Adafruit_PWMServoDriver.h>
#include <iostream>
#include <sstream>

class Leg {
    public: 
        int         leg_number;
        std::string leg_name;
        Actuator    joint_1;
        Actuator    joint_2;
        Actuator    joint_3;

        Adafruit_PWMServoDriver driver;

        Leg(int leg_number, std::string leg_name) {
            this->leg_number = leg_number;
            this->leg_name   = leg_name;
            this->driver = Adafruit_PWMServoDriver();
        }

        Leg(int leg_number, std::string leg_name, Actuator joint_1, Actuator joint_2, Actuator joint_3) {
            this->leg_number = leg_number;
            this->leg_name   = leg_name;
        
            this->joint_1 = joint_1;
            this->joint_2 = joint_2;
            this->joint_3 = joint_3;
            this->driver = Adafruit_PWMServoDriver();
        }

        std::string getStats() {
            std::string output_string; 
            output_string = "Leg Name:\t" + this->leg_name) + "\n";
            return output_string;
        }


        int angleToPulse(int angle, Actuator& actuator) {
          return map(angle, 0, 180,actuator->servo_min, actuator->servo_max);
        }

        void actuateLeg(int theta_1, int theta_2, int theta_3) {    
          this->driver.setPWM(this->joint_1.pin, 0, this->angleToPulse( (theta_1) + this->joint_1.offset, &this->joint_1));
          this->driver.setPWM(this->joint_2.pin, 0, this->angleToPulse( (theta_2) + this->joint_2.offset, &this->joint_2));
          this->driver.setPWM(this->joint_3.pin, 0, this->angleToPulse( (theta_3) + this->joint_3.offset, &this->joint_3));
        }

};







#endif // LEG_H
