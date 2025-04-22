#include <iostream>
#include <assert.h>
#include <stdlib.h>

struct Point{
int x; int y;
};
struct Shape{
enum EType {circle, square, rhombus};
EType type_;
};
struct Circle{
    Shape::EType type_;
    double radius_;
    Point center_;
};
struct Square{
    Shape::EType type_;
    double side_;
    Point center_;
};
struct Rhombus{
    Shape::EType type_;
    double side_;
    int angle;
    Point center_;
};
void drawSquare(struct Square*){
    std::cerr <<"in drawSquare\n";
}
void drawCircle(struct Circle*){
    std::cerr <<"in drawCircle\n";
}
void drawRhombus(struct Rhombus*){
    std::cerr <<"in drawRhombus\n";
}

void drawShapes(Shape** shapes, int n){
    for (int i=0; i<n; ++i){
        struct Shape* s = shapes[i];
        switch (s->type_){
            case Shape::square:
                drawSquare((struct Square*)s);
                break;
            case Shape::circle:
                drawCircle((struct Circle*)s);
                break;
            case Shape::rhombus:
                drawRhombus((struct Rhombus*)s);
                break;
            default:
            assert(0); 
            exit(0);
        }
    }
}

void moveShapes(Shape** shapes, int n, int dx, int dy) {
    for (int i = 0; i < n; i++) {
        if (shapes[i]->type_ == Shape::square) {
            Square* sq = (Square*)shapes[i];
            sq->center_.x += dx;
            sq->center_.y += dy;
        } else if (shapes[i]->type_ == Shape::circle) {
            Circle* cr = (Circle*)shapes[i];
            cr->center_.x += dx;
            cr->center_.y += dy;
        }
    }
}

void printPoints(Shape** shapes, int n) {
    for (int i = 0; i < n; i++) {
        if (shapes[i]->type_ == Shape::square) {
            Square* sq = (Square*)shapes[i];
            printf("%d,%d\n", sq->center_.x, sq->center_.y);
        } else if (shapes[i]->type_ == Shape::circle) {
            Circle* cr = (Circle*)shapes[i];
            printf("%d,%d\n", cr->center_.x, cr->center_.y);
        } else if (shapes[i]->type_ == Shape::rhombus) {
            Rhombus* rh = (Rhombus*)shapes[i];
            printf("%d,%d\n", rh->center_.x, rh->center_.y);
        }
    }
}

int main(){
    Shape* shapes[5];

    shapes[0] = (Shape*)new Circle;
    Circle* circle1 = (Circle*)shapes[0];
    circle1->type_ = Shape::circle;
    circle1->center_ = {0, 0};
    circle1->radius_ = 5.0;
    
    shapes[1] = (Shape*)new Square;
    Square* square1 = (Square*)shapes[1];
    square1->type_ = Shape::square;
    square1->center_ = {-1, -1};
    square1->side_ = 4.0;
    
    shapes[2] = (Shape*)new Square;
    Square* square2 = (Square*)shapes[2];
    square2->type_ = Shape::square;
    square2->center_ = {1, 1};
    square2->side_ = 6.0;
    
    shapes[3] = (Shape*)new Circle;
    Circle* circle2 = (Circle*)shapes[3];
    circle2->type_ = Shape::circle;
    circle2->center_ = {2, 1};
    circle2->radius_ = 3.0;

    shapes[4] = (Shape*)new Rhombus;
    Rhombus* rhombus = (Rhombus*)shapes[4];
    rhombus->type_ = Shape::rhombus;
    rhombus->center_ = {19098,5897};

    drawShapes(shapes, 5);
    moveShapes(shapes, 5, 1, 1);

    printPoints(shapes, 5);


    return 0;
}