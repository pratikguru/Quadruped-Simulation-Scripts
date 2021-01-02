#include <iostream>

using namespace std;

#define pi 3.14

double radians(int degrees)
{
    return degrees * (pi / 180);
}

double degrees(int radians)
{
    return radians * (180 / pi);
}

void rotate(int theta_1, int theta_2, int theta_3, int x, int y, int z)
{
    int theta1 = degrees(theta_1);
    int theta2 = degrees(theta_2);
    int theta3 = degrees(theta_3);

    auto row_1 = y * (cos(theta1) * sin(theta3) + cos(theta3) * sin(theta1) * sin(theta2)) +
                 z * (sin(theta1) * sin(theta3) - cos(theta1) * cos(theta3) * sin(theta2)) +
                 x * (cos(theta2) * cos(theta3));

    auto row_2 = y *
                     (cos(theta1) *
                          cos(theta3) -
                      sin(theta1) *
                          sin(theta2) *
                          sin(theta3)) +
                 z *
                     (cos(theta3) *
                          sin(theta1) +
                      cos(theta1) *
                          sin(theta2) *
                          sin(theta3)) -
                 x *
                     cos(theta2) *
                     sin(theta3);

    auto row_3 = x *
                     sin(theta_2) +
                 z * cos(theta_1) * cos(theta_2) -
                 y * cos(theta_2) * sin(theta_1);

    cout << row_1 << " " << row_2 << " " << row_3 << endl;
}

int main()
{
    rotate(0, 0, 0, 90, 90, 90);
}