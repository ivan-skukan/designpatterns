#include <iostream>
#include <list>

struct Point {
    int x;
    int y;
};

class Shape {
public:
    virtual void draw() = 0;
    virtual ~Shape() {}
};

class Circle : public Shape {
public:
    Circle(Point c, double r) : center_(c), radius_(r) {}
    void draw() override {
        std::cout << "Drawing Circle at (" << center_.x << "," << center_.y << ") with radius " << radius_ << "\n";
    }
private:
    Point center_;
    double radius_;
};

class Polyline : public Shape {
public:
    Polyline(Point c, double s) : center_(c), side_(s) {}
    void draw() override {
        std::cout << "Drawing Polyline centered at (" << center_.x << "," << center_.y << ") with side " << side_ << "\n";
    }
private:
    Point center_;
    double side_;
};

void drawShapes(const std::list<Shape*>& fig) {
    for (auto shape : fig) {
        shape->draw();
    }
}

int main() {
    std::list<Shape*> shapes;

    shapes.push_back(new Circle({0, 0}, 5.0));
    shapes.push_back(new Polyline({2, 3}, 8.0));
    shapes.push_back(new Circle({-1, -1}, 3.0));
    shapes.push_back(new Polyline({4, 4}, 2.5));

    drawShapes(shapes);

    // Clean up
    for (auto shape : shapes) {
        delete shape;
    }

    return 0;
}
