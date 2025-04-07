#include <iostream>

class B{
    public:
      virtual int prva()=0;
      virtual int druga(int)=0;
    };
    
class D: public B{
    public:
      virtual int prva(){return 42;}
      virtual int druga(int x){return prva()+x;}
};


void task(B* pb) {
    void** vtable = *(void***)pb;

    using Fn1 = int(*)(B*);
    Fn1 f1 = (Fn1)vtable[0]; // kako zna offset?
    std::cout << f1(pb) << std::endl;

    using Fn2 = int(*)(B*, int);
    Fn2 f2 = (Fn2)vtable[1];
    std::cout << f2(pb, 10) << std::endl;
}



int main() {
    B* pb = new D();
    task(pb);
    delete pb;
    /* D d;
    B* pb = &d;
    task(pb); */
    return 0;
}