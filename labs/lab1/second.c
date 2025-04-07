#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>


typedef struct Unary_Function Unary_Function;

typedef double (*UFUNCS_VALUEAT)(Unary_Function*, int);
typedef double (*UFUNCS_NEGVALUEAT)(Unary_Function*, int);

typedef struct {
    UFUNCS_VALUEAT valueat;
    UFUNCS_NEGVALUEAT nvalueat;
} UF_vtable;

struct Unary_Function {
    int lower_bound;
    int upper_bound;
    UF_vtable* vtable;
};

typedef struct {
    Unary_Function unary_parent; // shared state across multiple child objects?
} Square;

typedef struct {
    Unary_Function unary_parent;
    double a;
    double b;
} Linear;

double nvalueat(Unary_Function*  unary, int x) {
    return -unary->vtable->valueat(unary, x);
}
void tabulate(Unary_Function* unary){ 
    for (int x = unary->lower_bound; x <= unary->upper_bound; x++) { 
        printf("f(%d)=%lf\n", x, unary->vtable->valueat(unary, x));
    } 
}

double square_valueat(Unary_Function* unary, int x) {return x*x;} // unary or square? cast?
double linear_valueat(Unary_Function* unary, int x) {
    Linear* linear = (Linear*) unary;
    return linear->a * x + linear->b;
}

bool same_functions_for_ints(Unary_Function *f1, Unary_Function *f2, double tolerance) {
    if (f1->lower_bound != f2->lower_bound || f1->upper_bound != f2->upper_bound) 
        return false;

    for (int x = f1->lower_bound; x <= f1->upper_bound; x++) {
        double delta = f1->vtable->valueat(f1, x) - f2->vtable->valueat(f2, x);
        if (delta < 0) delta = -delta;
        if (delta > tolerance) return false;
    }
    return true;
}

UF_vtable square_funcs = {
    .valueat = square_valueat,
    .nvalueat = nvalueat
};

UF_vtable linear_funcs = {
    .valueat = linear_valueat,
    .nvalueat = nvalueat
};

void constructor_Unary(Unary_Function* uf, int lb, int ub, UF_vtable* funcs) { //void and cast?
    //printf("ConstructorUnary\n");
    uf->lower_bound = lb;
    uf->upper_bound = ub;
    uf->vtable = funcs;
}

void constructor_Square(Square* sq, int lb, int ub) { // gpt kaze da brises ovo
    //printf("Constructsq\n");
    Unary_Function uf;
    constructor_Unary(&uf, lb, ub, &square_funcs);
    sq->unary_parent = uf;
    sq->unary_parent.vtable->valueat = square_valueat;
}

void constructor_Linear(Linear* lin, int lb, int ub, double a, double b) {
    Unary_Function uf;
    constructor_Unary(&uf, lb, ub, &linear_funcs);
    lin->unary_parent = uf;
    lin->unary_parent.vtable->valueat = linear_valueat;
    lin->a = a;
    lin->b = b;
}

Square* createSquare(int lb, int ub) {
    //printf("Createsq\n");
    Square* sq = (Square*)malloc(sizeof(Square));
    constructor_Square(sq, lb, ub);
    //printf("Fin createsq\n");
    return sq;
}

Linear* createLinear(int lb, int ub, double a, double b) {
    Linear* lin = (Linear*)malloc(sizeof(Linear));
    constructor_Linear(lin, lb, ub, a, b);

    return lin;
}

int main(int argc, char** argv) {
    int lb = -2; int ub = 2;
    
    // heap
    Unary_Function* square = (Unary_Function*)createSquare(lb,ub);
    printf("%zu\n", sizeof(*square));
    tabulate(square);
    int a = 5; int b = -2;
    Unary_Function* linear = (Unary_Function*)createLinear(lb,ub, a, b);
    printf("%zu\n", sizeof(*linear));
    tabulate(linear);
    printf("f1==f2: %s\n", same_functions_for_ints(square, linear, 1E-6) ? "DA" : "NE");
    printf("neg_val f2(1) = %lf\n", linear->vtable->nvalueat(linear, 1.0));
    free(square);
    free(linear);
    printf("Stack test\n");
    Square sq_stack;
    constructor_Square(&sq_stack, lb, ub);
    tabulate(&sq_stack.unary_parent);

    return 0;
}