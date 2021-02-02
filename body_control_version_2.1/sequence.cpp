#include <iostream>

using namespace std;

int main()
{

  int sequence[][4][3] = {
      {{3, 4, 2}, {0, -3, 9}, {23, 12, 23}, {23, 12, 23}},
      {{13, 4, 56}, {5, 9, 3}, {5, 1, 4}, {23, 12, 23}}};

  for (int i = 0; i < 2; i++)
  {
    cout << sequence[i][0][0] << sequence << endl;
  }
}