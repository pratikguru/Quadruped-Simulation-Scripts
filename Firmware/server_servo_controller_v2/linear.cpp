#include<iostream>


using namespace std;

int main()
{
 float x0,y0,x1,y1,xp,yp;

 /* Inputs */

 x0 = 50;
 y0 = 40;
 
 x1 = 50;
 y1 = 60;




 /* Linear Interpolation */
 for(int i = 0; i < 50; i++) {
      xp = i;
      yp = y0 + ((y1-y0)/(x1-x0)) * (xp - x0);
      cout<<"Interpolated value at "<< xp<<" is "<< yp << endl;
 }





 return 0;
}
