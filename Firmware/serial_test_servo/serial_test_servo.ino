#include <Adafruit_PWMServoDriver.h>
#define SERVOMIN 100 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 600 // this is the 'maximum' pulse length count (out of 4096)
#define LINK_1 60
#define LINK_2 120
#define LINK_3 80

Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver();

struct ServoObj
{
  int pin;
  int offset;

  ServoObj(int pin, int offset)
  {
    this->pin = pin;
    this->offset = offset;
  }
};

ServoObj leg_1_1(0, 0);
ServoObj leg_1_2(1, 30);
ServoObj leg_1_3(2, 0);

ServoObj leg_2_1(4, 0);
ServoObj leg_2_2(5, 30);
ServoObj leg_2_3(6, 0);

ServoObj leg_3_1(8, 10);
ServoObj leg_3_2(9, 30);
ServoObj leg_3_3(10, 0);

ServoObj leg_4_1(12, 10);
ServoObj leg_4_2(13, 42);
ServoObj leg_4_3(15, 0);

ServoObj servos[] = {
    leg_1_1, leg_1_2, leg_1_3,
    leg_2_1, leg_2_2, leg_2_3,
    leg_3_1, leg_3_2, leg_3_3,
    leg_4_1, leg_4_2, leg_4_3};

struct Angles
{
  double theta_1;
  double theta_2;
  double theta_3;

  Angles()
  {
    this->theta_1 = 0;
    this->theta_2 = 0;
    this->theta_3 = 0;
  }

  Angles(double theta_1, double theta_2, double theta_3)
  {
    this->theta_1 = theta_1;
    this->theta_2 = theta_2;
    this->theta_3 = theta_3;
  }
};

void up(int leg)
{
  getIk(0, 60, 40, leg);
}

void down(int leg)
{
  getIk(0, 50, 60, leg);
}

void frontUp(int leg)
{
  getIk(10, 50, 40, leg);
}

void frontDown(int leg)
{

  getIk(10, 50, 50, leg);
}

void backDown(int leg)
{
  getIk(-10, 50, 50, leg);
}

void backUp(int leg)
{
  getIk(-10, 50, 40, leg);
}

void getIk(int x, int y, int z, int leg)
{
  auto theta_1 = atan2(y, x);
  auto A = z;
  auto B = cos(theta_1) * x + y + sin(theta_1) - LINK_1;
  auto C = ((pow(A, 2) + pow(B, 2) - pow(LINK_3, 2) - pow(LINK_2, 2)) / (2 * LINK_3 * LINK_2));
  auto theta_3 = atan2(sqrt(1 - pow(C, 2)), C);

  auto D = (cos(theta_3) * LINK_3) + LINK_2;
  auto E = sin(theta_3) * LINK_3;
  auto numerator = (A * D - B * E) / (pow(E, 2) + pow(D, 2));
  auto denominator = 1 - pow(numerator, 2);
  auto theta_2 = atan2(numerator, sqrt(denominator));
  int angleToPulse(int ang);

  theta_1 = degrees(theta_1);
  theta_2 = degrees(theta_2);
  theta_3 = degrees(theta_3);

  if (isnan(theta_1) || isnan(theta_2) || isnan(theta_3))
  {
    Serial.println(String("x: " + String(x) + " y: " + String(y) + " z: " + String(z)));
    return;
  }

  switch (leg)
  {
  case 1:
  {
    pwm.setPWM(servos[0].pin, 0, angleToPulse((theta_1) + servos[0].offset));
    pwm.setPWM(servos[1].pin, 0, angleToPulse((theta_2) + servos[1].offset));
    pwm.setPWM(servos[2].pin, 0, angleToPulse((theta_3) + servos[2].offset));
    break;
  }
  case 2:
  {
    pwm.setPWM(servos[3].pin, 0, angleToPulse((theta_1) + servos[3].offset));
    pwm.setPWM(servos[4].pin, 0, angleToPulse((theta_2) + servos[4].offset));
    pwm.setPWM(servos[5].pin, 0, angleToPulse((theta_3) + servos[5].offset));
    break;
  }
  case 3:
  {
    pwm.setPWM(servos[6].pin, 0, angleToPulse((theta_1) + servos[6].offset));
    pwm.setPWM(servos[7].pin, 0, angleToPulse((theta_2) + servos[7].offset));
    pwm.setPWM(servos[8].pin, 0, angleToPulse((theta_3) + servos[8].offset));
    break;
  }
  case 4:
  {
    pwm.setPWM(servos[9].pin, 0, angleToPulse((theta_1) + servos[9].offset));
    pwm.setPWM(servos[10].pin, 0, angleToPulse((theta_2) + servos[10].offset));
    pwm.setPWM(servos[11].pin, 0, angleToPulse((theta_3) + servos[11].offset));
    break;
  }
  }
  Serial.println(String(x) + " " + String(y) + " " + String(z) + " " + String((theta_1)) + " " + String((theta_2)) + " " + String((theta_3)));
}

int globalX = 0;
int globalY = 65;
int globalZ = 40;

// 40, 20, 40 - up-back
// 0, 60, 40 - up-center
// -40, 20, 40

//0, 50, 60 - down-center
//40, 20, 60 - down-back
// -40, 20, 60

void setup()
{
  Serial.begin(115200);
  pwm.begin();
  pwm.setPWMFreq(60);

  getIk(globalX, globalY, globalZ, 1);
  getIk(globalX, globalY, globalZ, 2);
  getIk(globalX, globalY, globalZ, 3);
  getIk(globalX, globalY, globalZ, 4);
}

void loop()
{

  while (!Serial.available())
  {
  }

  while (Serial.available())
  {
    String incoming = Serial.readStringUntil('\n');
    if (incoming == "+")
    {
      globalX += 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }

    else if (incoming == "++")
    {
      globalY += 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }

    else if (incoming == "+++")
    {
      globalZ += 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }

    else if (incoming == "-")
    {
      globalX -= 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }

    else if (incoming == "--")
    {
      globalY -= 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }

    else if (incoming == "---")
    {
      globalZ -= 5;
      getIk(globalX, globalY, globalZ, 1);
      // getIk(globalX, globalY, globalZ, 2);
      // getIk(globalX, globalY, globalZ, 3);
      // getIk(globalX, globalY, globalZ, 4);
    }
  }
}

int angleToPulse(int ang)
{
  int pulse = map(ang, 0, 180, SERVOMIN, SERVOMAX); // map angle of 0 to 180 to Servo min and Servo max

  return pulse;
}
