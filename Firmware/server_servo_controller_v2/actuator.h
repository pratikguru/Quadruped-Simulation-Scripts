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

        int link_length = 60;

    Actuator(){
        this->pin = 0;
        this->offset = 0;
        this->servo_min = 100;
        this->servo_max = 600;
        this->link_length = 60;
    }

    Actuator(int pin, int offset, int link_length) {
        this->pin = pin;
        this->offset = offset;
        this->servo_min = 100;
        this->servo_max = 600;
        this->link_length = link_length;
    }

    Actuator(int pin, int offset, int servo_min, int servo_max, int link_length) {
        this->pin = pin;
        this->offset = offset;
        this->servo_min = servo_min;
        this->servo_max = servo_max;
        this->link_length = link_length;
    }
};

#endif //ACTUATOR_H
