#include <iostream>

using namespace std;

struct Point {
    float x, y;
};

Point operator+ (Point const &pt1, Point const &pt2) {
    return { pt1.x + pt2.x, pt1.y + pt2.y };
}

Point operator- (Point const &pt1, Point const &pt2) {
    return { pt1.x - pt2.x, pt1.y - pt2.y };
}

Point scale(Point const &pt, float t) {
    return { pt.x * t, pt.y * t };
}

std::ostream& operator<<(std::ostream &os, Point const &pt) {
    return os << '{' << pt.x << ", " << pt.y << '}' << ",";
}

void lerp(Point const &pt1, Point const &pt2, float stops) {
    Point const v = pt2 - pt1;
    float t = 0.0f;
    for (float i = 0.0f; i <= stops; ++i) {
        t = i / stops;
        Point const p = pt1 + scale(v, t);
        
        std::cout << p << "\n";
        
    }
}

int main() {
    Point pt1;
    pt1.x = -30;
    pt1.y = 40;

    Point pt2;
    pt2.x = 30;
    pt2.y = 80;
    lerp(pt1, pt2, 50);
}