#ifndef LEG_H
#define LEG_H 
#include "actuator.h"
#include <Adafruit_PWMServoDriver.h>

#include "vector.h"

class Leg {
    public: 
        int         leg_number;
        String      leg_name;
        

        Actuator    joint_1;
        Actuator    joint_2;
        Actuator    joint_3;
        
        Adafruit_PWMServoDriver driver;
        IK          ik;
        
        Leg(int leg_number, String leg_name) {
            this->leg_number = leg_number;
            this->leg_name   = leg_name;
            this->driver = Adafruit_PWMServoDriver();
            this->driver.begin();
            this->driver.setPWMFreq(60);
            
        }

        Leg(int leg_number, String leg_name, Actuator joint_1, Actuator joint_2, Actuator joint_3) {
            this->leg_number = leg_number;
            this->leg_name   = leg_name;
        
            this->joint_1 = joint_1;
            this->joint_2 = joint_2;
            this->joint_3 = joint_3;
            this->driver = Adafruit_PWMServoDriver();
            this->driver.begin();
            this->driver.setPWMFreq(60);
            IK ik(joint_1.link_length, joint_2.link_length, joint_3.link_length);
            this->ik = ik;
            
        }

        String getStats() {
            String output_string; 
            output_string = "Leg Name:\t" + (this->leg_name) + "\n" \ 
            + "Leg Number:\t" + (this->leg_number) + "\n" \ 
            + "Tibia Pin:\t" + (this->joint_1.pin) + "\n" \ 
            + "Coxa Pin:\t" + (this->joint_2.pin)  + "\n" \ 
            + "Femur Pin:\t" + (this->joint_3.pin) + "\n";
            return output_string;
        }


        int moveLeg(int x, int y, int z) {
          Vector output; 
          output = this->ik.getIk(x, y, z);
          Serial.println(String(output.theta_1) + " " + String(output.theta_2) + " " + String(output.theta_3));
          this->actuateLeg( output.theta_1, output.theta_2, output.theta_3);
          return 0;
        }
        
        int angleToPulse(int angle, Actuator& actuator) {
          return map(angle, 0, 180,actuator.servo_min, actuator.servo_max);
        }

        void actuateLeg(int theta_1, int theta_2, int theta_3) {   
          
          this->driver.setPWM(this->joint_1.pin, 0, this->angleToPulse( (theta_1) + this->joint_1.offset, this->joint_1));
          this->driver.setPWM(this->joint_2.pin, 0, this->angleToPulse( (theta_2) + this->joint_2.offset, this->joint_2));
          this->driver.setPWM(this->joint_3.pin, 0, this->angleToPulse( (theta_3) + this->joint_3.offset, this->joint_3));
        }

};

#endif // LEG_H
