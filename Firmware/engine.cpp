#include <iostream>
#include <cmath>

#define LINK_1 60
#define LINK_2 120
#define LINK_3 60
void print(std::string value)
{
    std::cout << value << std::endl;
    return;
};

struct Angles
{
    int theta_1;
    int theta_2;
    int theta_3;

    Angles(int theta_1, int theta_2, int theta_3)
    {
        this->theta_1 = theta_1;
        this->theta_2 = theta_2;
        this->theta_3 = theta_3;
    }
};

struct Angles getIk(int x, int y, int z)
{
    auto theta_1 = atan2(y, x);
    std::cout << theta_1 << std::endl;
    auto A = z;
    auto B = cos(theta_1) * x + y + sin(theta_1) - LINK_1;
    std::cout << B << std::endl;

    auto C = ((pow(A, 2) + pow(B, 2) - pow(LINK_3, 2) - pow(LINK_2, 2)) / (2 * LINK_3 * LINK_2));
    std::cout << C << std::endl;

    auto theta_3 = atan2(sqrt(1 - pow(C, 2)), C);
    std::cout << theta_3 << std::endl;
    theta_3 = 1.9022543427753416;
    auto D = (cos(theta_3) * LINK_3) + LINK_2;
    auto E = sin(theta_3) * LINK_3;
    std::cout << D << std::endl;
    std::cout << E << std::endl;
    auto numerator = (A * D - B * E) / (pow(E, 2) + pow(D, 2));
    auto denominator = 1 - pow(numerator, 2);
    auto theta_2 = atan2(numerator, sqrt(denominator));

    std::cout << numerator << std::endl;
    std::cout << denominator << std::endl;
    std::cout << theta_2 << std::endl;

    theta_1 = degrees(theta_1);
    theta_2 = degrees(theta_2);
    theta_3 = degrees(theta_3);

    return Angles(theta_1, theta_2, theta_3);
}

int main()
{
    getIk(100, 100, -30);
}
