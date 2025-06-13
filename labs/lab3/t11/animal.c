#include <stdio.h>
#include <stdlib.h>
#include "myfactory.h"


typedef char const* (*PTRFUN)();

typedef struct {
  PTRFUN* vtable;
  char const* name;
} Animal;


void animalPrintGreeting(Animal* p){
  printf("%s pozdravlja: %s\n", p->vtable[0](p), p->vtable[1]());
}

void animalPrintMenu(Animal* p){
  printf("%s voli %s\n", p->vtable[0](), p->vtable[2]());
}