#include <iostream>

class CoolClass{
    public:
      virtual void set(int x){x_=x;};
      virtual int get(){return x_;};
    private:
      int x_;
};
class PlainOldClass{
    public:
        void set(int x){x_=x;};
        int get(){return x_;};
    private:
        int x_;
};

struct A {
    //char c; // 4 without, 8 with
    int x;
};

struct B {
    char a;  // 1 byte
    short b; // 2 bytes
    char c;  // 1 byte
};

int main() {
    std::cout << "Size of CoolClass: " << sizeof(CoolClass) << std::endl;
    std::cout << "Size of PlainOldClass: " << sizeof(PlainOldClass) << std::endl;
    std::cout << "Size of A:" << sizeof(A) << std::endl;
    std::cout << "Size of B:" << sizeof(B) << std::endl;
}


// PlainOldClass ima samo 1 int - 4 bajta
// CoolClass - int je 4
//           - 