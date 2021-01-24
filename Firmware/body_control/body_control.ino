#include <Adafruit_PWMServoDriver.h>
#include <WiFi.h>
#include <Wire.h>

#define SERVOMIN 100 // this is the 'minimum' pulse length count (out of 4096)
#define SERVOMAX 600 // this is the 'maximum' pulse length count (out of 4096)
#define LINK_1 60
#define LINK_2 120
#define LINK_3 80
#define RUN_ROBOT_ON_SERVER true
#define STATIC_SERVER_CREDENTIALS false


int power_pin = 14;
Adafruit_PWMServoDriver pwm = Adafruit_PWMServoDriver(0x40);


//yellow - scl - 22
//red - sda - 21

//const char *ssid = "robotyka_564";
//const char *password = "shamrock12345";
char* ssid     = "UPCD736725";
char* password = "Y6Zcwbtruurb";
//const char* ssid = "FD-43";
//const char* password = "";

IPAddress local_IP(10, 0, 0, 1);
IPAddress gateway(10, 0, 0, 1);
IPAddress subnet(255, 255, 0, 0);
IPAddress primaryDNS(8, 8, 8, 8);   //optional
IPAddress secondaryDNS(8, 8, 4, 4); //optional
WiFiServer server(80);

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
ServoObj leg_1_2(1, 0);
ServoObj leg_1_3(3, 0);

ServoObj leg_2_1(4, 15);
ServoObj leg_2_2(5, 0);
ServoObj leg_2_3(6, 0);

ServoObj leg_3_1(8, 10);
ServoObj leg_3_2(9, 0);
ServoObj leg_3_3(10, 0);

ServoObj leg_4_1(12, -10);
ServoObj leg_4_2(13, 0);
ServoObj leg_4_3(14, 0);

ServoObj servos[] = {
  leg_1_1, leg_1_2, leg_1_3,
  leg_2_1, leg_2_2, leg_2_3,
  leg_3_1, leg_3_2, leg_3_3,
  leg_4_1, leg_4_2, leg_4_3
};

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

struct Vector
{
  int x;
  int y;
  int z;

  Vector()
  {
    this->x = 0;
    this->y = 0;
    this->z = 0;
  }

  Vector(int x, int y, int z)
  {
    this->x = x;
    this->y = y;
    this->z = z;
  }
};

void up(int leg)
{
  getIk(0, 60, 40, leg);
}

void down(int leg)
{
  getIk(0, 45, 60, leg);
}

void frontUp(int leg)
{
  getIk(10, 20, 40, leg);
}

void frontDown(int leg)
{

  getIk(10, 20, 45, leg);
}

void backDown(int leg)
{
  getIk(-30, 20, 45, leg);
}

void backUp(int leg)
{
  getIk(-30, 20, 40, leg);
}

Vector rotate(int theta_1, int theta_2, int theta_3, int x, int y, int z)
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
  Vector vector(row_1, row_2, row_3);
  return vector;
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
  //Serial.println(String(x) + " " + String(y) +  " " + String(z) + " " + String((theta_1)) + " " + String((theta_2)) + " " + String((theta_3)));
}

int globalX = 0;
int globalY = 60;
int globalZ = 40;

int translateX = 0;
int translateY = 0;
int translateZ = 0;

bool bounceMode = true;

int maxDataPoints = 50;
int minDataPoints = 0;

void checkConnection() {
  byte error, address;
  int nDevices;

  Serial.println("Scanning...");

  nDevices = 0;
  for (address = 1; address < 127; address++ )
  {

    Wire.beginTransmission(address);
    error = Wire.endTransmission();

    if (error == 0)
    {
      Serial.print("I2C device found at address 0x");
      if (address < 16)
        Serial.print("0");
      Serial.print(address, HEX);
      Serial.println("  !");

      nDevices++;
    }
    else if (error == 4)
    {
      Serial.print("Unknown error at address 0x");
      if (address < 16)
        Serial.print("0");
      Serial.println(address, HEX);
    }
  }
  if (nDevices == 0)
    Serial.println("No I2C devices found\n");
  else
    Serial.println("done\n");
  delay(5000);
}

void setup()
{
  Serial.begin(115200);
  pwm.begin();
  
  pwm.setPWMFreq(60);
  yield();
  
  
  
  pinMode(power_pin, OUTPUT);
  digitalWrite(power_pin, HIGH);
#if RUN_ROBOT_ON_SERVER
  Serial.print("Connecting to ");
  Serial.println(ssid);

#if STATIC_SERVER_CREDENTIALS
  Serial.println("Setting Static Server Credentials");
  if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS))
  {
    Serial.println("Static settings failure");
  }
#endif
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(400);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
#else
  Serial.println("No Server Running");
#endif

  getIk(globalX, globalY, globalZ, 1);
  getIk(globalX, globalY, globalZ, 2);
  getIk(globalX, globalY, globalZ, 3);
  getIk(globalX, globalY, globalZ, 4);

  Serial.println("Pose Ready");
  down(1);
  down(2);
  down(3);
  down(4);
  
}

void loop()
{
  WiFiClient client = server.available(); // listen for incoming clients

  if (client)
  {
    while (client.connected())
    {
      int byteSize = 0;
      uint8_t dataPacket[256];

      if (byteSize = client.available())
      {
        for (int i = 0; i < byteSize; i++)
        {
          dataPacket[i] = client.read();
          Serial.print(dataPacket[i]);
        }
        Serial.println();
        if (dataPacket[0] > 20)
        {
          return;
        }

        if (dataPacket[0] == 1)
        {
          Serial.println("Z-Translate ");
          getIk(map(dataPacket[1], 0, 40, -40, 40), dataPacket[5], dataPacket[9], 1);
          getIk(map(dataPacket[2], 0, 40, -40, 40), dataPacket[6], dataPacket[10], 2);
          getIk(map(dataPacket[3], 0, 40, -40, 40), dataPacket[7], dataPacket[11], 3);
          getIk(map(dataPacket[4], 0, 40, -40, 40), dataPacket[8], dataPacket[12], 4);
        }
        else if (dataPacket[0] == 2)
        {
          Serial.println("Z-Rotate");
          Serial.println(globalZ);
          getIk(map(dataPacket[1], 0, 40, -40, 40), 40, dataPacket[2], 1);
          getIk(map(dataPacket[1], 0, 40, -40, 40), 40, dataPacket[2], 2);
          getIk(map(dataPacket[1], 0, 40, -40, 40), 40, dataPacket[2], 3);
          getIk(map(dataPacket[1], 0, 40, -40, 40), 40, dataPacket[2], 4);
        }

        else if (dataPacket[0] == 3)
        {
          Serial.println("Going to home position");
          getIk(globalX, globalY, globalZ, 1);
          getIk(globalX, globalY, globalZ, 2);
          getIk(globalX, globalY, globalZ, 3);
          getIk(globalX, globalY, globalZ, 4);
        }

        else if (dataPacket[0] == 4)
        {
          down(1);
          down(2);
          down(3);
          down(4);

          delay(100);
          up(1);
          delay(90);
          backUp(1);
          delay(90);
          backDown(1);

          delay(100);
          up(3);
          delay(90);
          backUp(3);
          delay(90);
          backDown(3);

          delay(100);
          up(4);
          delay(90);
          backUp(4);
          delay(90);
          backDown(4);

          delay(100);
          up(2);
          delay(90);
          backUp(2);
          delay(90);
          backDown(2);

          delay(100);
          down(1);
          down(2);
          down(3);
          down(4);
          return;
        }

        else if (dataPacket[0] == 5)
        {

          up(1);
          up(3);

          down(2);
          down(4);

          delay(120);

          up(2);
          up(4);

          down(1);
          down(3);
          delay(120);
        }
      }
    }
  }
}

int angleToPulse(int ang)
{
  int pulse = map(ang, 0, 180, SERVOMIN, SERVOMAX); // map angle of 0 to 180 to Servo min and Servo max
  return pulse;
}
