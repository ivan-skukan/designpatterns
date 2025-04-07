// Function pointers
typedef void (*UFUNCS_CONST)(void* ufunc, int lb, int ub);
typedef void (*UFUNCS_TABULATE)(void* ufunc);
typedef double (*UFUNCS_VALUEAT)(void* ufunc, int x); // This will take a struct pointer (self) and an x value.
typedef double (*UFUNCS_NEGVALUEAT)(void* ufunc, int x); // This also needs to take self and x.

// A struct to hold function pointers for each derived class.
typedef struct {
    UFUNCS_CONST constructor;
    UFUNCS_TABULATE tabulate;
    UFUNCS_VALUEAT value_at;  // Set in the derived class
    UFUNCS_NEGVALUEAT negative_value_at;  // This can be shared, so it's set by default in the base class
} Unary_funcs;

// Base class struct (Unary_Function_Class)
typedef struct {
    int lower_bound;
    int upper_bound;
    Unary_funcs* func_table;  // Function table for dynamic dispatch
} Unary_Function_Class;

// Derived class: Square
typedef struct {
    Unary_Function_Class base;  // Inherit from Unary_Function_Class
} Square;

// Derived class: Linear
typedef struct {
    Unary_Function_Class base;  // Inherit from Unary_Function_Class
    double a;
    double b;
} Linear;

// Constructor for the base class (Unary_Function_Class)
void constructor_Unary(Unary_Function_Class* uf, int lb, int ub) {
    uf->lower_bound = lb;
    uf->upper_bound = ub;
    uf->func_table = &ufuncs_table; // Set the function table for the derived class
}

// Constructor for Square (derived class)
void constructor_Square(Square* sq, int lb, int ub) {
    constructor_Unary((Unary_Function_Class*)sq, lb, ub);
    sq->base.func_table->value_at = square_value_at;  // Set the derived class-specific function
    sq->base.func_table->negative_value_at = negative_value_at; // Set the shared negative_value_at function
}

// Constructor for Linear (derived class)
void constructor_Linear(Linear* lin, int lb, int ub, double a, double b) {
    constructor_Unary((Unary_Function_Class*)lin, lb, ub);
    lin->base.func_table->value_at = linear_value_at;  // Set the derived class-specific function
    lin->base.func_table->negative_value_at = negative_value_at; // Set the shared negative_value_at function
}

// Function for calculating value for Square (derived class)
double square_value_at(void* ufunc, int x) {
    return x * x;
}

// Function for calculating value for Linear (derived class)
double linear_value_at(void* ufunc, int x) {
    Linear* lin = (Linear*)ufunc;
    return lin->a * x + lin->b;
}

// Function for negative value calculation (can be shared by all derived classes)
double negative_value_at(void* ufunc, int x) {
    return -ufunc->func_table->value_at(ufunc, x);  // Call the value_at function of the derived class and negate it
}

// Function to tabulate (print the values for the function)
void tabulate(Unary_Function_Class* uf) {
    for (int x = uf->lower_bound; x <= uf->upper_bound; x++) {
        printf("f(%d) = %lf\n", x, uf->func_table->value_at(uf, x));
    }
}

// Function to create and initialize a Square
Square* createSquare(int lb, int ub) {
    Square* sq = malloc(sizeof(Square));
    constructor_Square(sq, lb, ub);
    return sq;
}

// Function to create and initialize a Linear
Linear* createLinear(int lb, int ub, double a, double b) {
    Linear* lin = malloc(sizeof(Linear));
    constructor_Linear(lin, lb, ub, a, b);
    return lin;
}

// Function to compare two functions (not implemented in this example)
bool same_functions_for_ints(Unary_Function_Class* f1, Unary_Function_Class* f2, double tolerance) {
    // Compare functions based on the value_at results and return true/false based on tolerance
    return true;
}

int main() {
    // Create Square and Linear objects
    Unary_Function_Class* f1 = (Unary_Function_Class*)createSquare(-2, 2);
    f1->func_table->tabulate(f1);
    
    Unary_Function_Class* f2 = (Unary_Function_Class*)createLinear(-2, 2, 5, -2);
    f2->func_table->tabulate(f2);
    
    // Check if the functions are the same within a tolerance
    printf("f1==f2: %s\n", same_functions_for_ints(f1, f2, 1E-6) ? "YES" : "NO");
    
    // Negate the value for Linear at x=1
    printf("neg_val f2(1) = %lf\n", f2->func_table->negative_value_at(f2, 1.0));
    
    // Clean up
    free(f1);
    free(f2);
    
    return 0;
}
