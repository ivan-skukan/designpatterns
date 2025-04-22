#include <stdio.h>
#include <string.h>

int gt_int(const void* a, const void* b) {
    int arg1 = *(const int*)a;
    int arg2 = *(const int*)b;

    return arg1 > arg2;
}

int gt_char(const void* a, const void* b) { 
    char arg1 = *(const char*)a;
    char arg2 = *(const char*)b;
    
    return arg1 > arg2;
}

int gt_str(const void* a, const void* b) {
    const char* arg1 = *(const char**)a; const char* arg2 = *(const char**)b;
    return strcmp(arg1,arg2);
}
r
const void* mymax(
    const void *base, size_t nmemb, size_t size,
    int (*compar)(const void*, const void*)) {
        size_t argmax = 0;

        for (size_t i = 1; i < nmemb; i++) {
            if (compar(base+i*size, base+argmax*size)>0) { //*
                argmax = i;
            }
        }

        return base + argmax*size; //*
}
// * this only works because of implicit conversion to char*

int main() {
    int arr_int[] = { 1, 3, 5, 7, 4, 6, 9, 2, 0 };
    char arr_char[]="Suncana strana ulice";
    const char* arr_str[] = {
        "Gle", "malu", "vocku", "poslije", "kise",
        "Puna", "je", "kapi", "pa", "ih", "njise"
    };


    const void* max = mymax(arr_int, 9, 4, gt_int);
    printf("%d\n", *(const int*)max);

    max = mymax(arr_char, 20, 1, gt_char);
    printf("%c\n", *(const char*)max);

    max = mymax(arr_str, 11, 8, gt_str); // why does this work considering its **
    printf("%s\n", *(const char**)max);
    return 0;
}