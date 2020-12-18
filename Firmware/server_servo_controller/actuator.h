#ifndef ACTUATOR_H
#define ACTUATOR_H

#define SERVOMIN 100 
#define SERVOMAX 600



class Actuator {
    public: 
        int pin;
        int offset;

        int servo_min = 100;
        int servo_max = 600;

    Actuator(){
        this->pin = 0;
        this->offset = 0;
        this->servo_min = 100;
        this->servo_max = 600;
    }

    Actuator(int pin, int offset) {
        this->pin = pin;
        this->offset = offset;
        this->servo_min = 100;
        this->servo_max = 600;
    }

    Actuator(int pin, int offset, int servo_min, int servo_max) {
        this->pin = pin;
        this->offset = offset;
        this->servo_min = servo_min;
        this->servo_max = servo_max;
    }






};

#endif //ACTUATOR_H
