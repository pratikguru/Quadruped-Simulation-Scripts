#ifndef IK_H
#define IK_H 
#include "vector.h"



class IK {
    public: 
        int link_1;
        int link_2;
        int link_3;
        
        
        IK() {
          this->link_1 = 0;
          this->link_2 = 0;
          this->link_3 = 0;
        }

        IK(int link_1, int link_2, int link_3) {
          this->link_1 = link_1;
          this->link_2 = link_2;
          this->link_3 = link_3;
        }

        Vector getIk( int x, int y, int z) {
          auto theta_1 = atan2(y, x);
          auto A = z;
          auto B = cos(theta_1) * x + y + sin(theta_1) - this->link_1;
          auto C = ((pow(A, 2) + pow(B, 2) - pow(this->link_3, 2) - pow(this->link_2, 2)) / (2 * this->link_3 * this->link_2));
          auto theta_3 = atan2(sqrt(1 - pow(C, 2)), C);
        
          auto D = (cos(theta_3) * this->link_3) + this->link_2;
          auto E = sin(theta_3)  * this->link_3;
          auto numerator = (A * D - B * E) / (pow(E, 2) + pow(D, 2));
          auto denominator = 1 - pow(numerator, 2);
          auto theta_2 = atan2(numerator, sqrt(denominator));
          int angleToPulse(int ang);
          
          theta_1 = degrees(theta_1);
          theta_2 = degrees(theta_2);
          theta_3 = degrees(theta_3);
          if(isnan(theta_1) || isnan(theta_2)  || isnan(theta_3) ) {
             Serial.println(String("x: "+ String(x) + " y: " + String(y) + " z: " + String(z)));
             Vector vector;
             return vector;
          }

          
          Vector vector(theta_1, theta_2, theta_3);
          return vector;
        }
        

};


#endif //IK_H
