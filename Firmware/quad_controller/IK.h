#ifndef IK_H
#define IK_H 



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

}


#endif //IK_H