#ifndef VECTOR_H
#define VECTOR_H 




class Vector {
  public:
    int theta_1;
    int theta_2;
    int theta_3;

  Vector(){
    this->theta_1 = 90;
    this->theta_2 = 90;
    this->theta_3 = 90;
  }

  Vector(int theta_1, int theta_2, int theta_3) {
    this->theta_1 = theta_1;
    this->theta_2 = theta_2;
    this->theta_3 = theta_3;
  }
};

#endif //VECTOR_H
