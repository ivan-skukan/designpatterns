#include "myfactory.h"
#include <stdio.h>
#include <stdlib.h>

typedef char const* (*PTRFUN)();


/* typedef struct {
  PTRFUN name;
  PTRFUN greet;
  PTRFUN menu;
} vtable; */

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



int main(int argc, char *argv[]){
  for (int i=0; i<argc/2; ++i){


    Animal* p=(Animal*)myfactory(argv[1+2*i], argv[1+2*i+1], NULL);
    if (!p){
      printf("Creation of plug-in object %s failed.\n", argv[1+2*i]);
      continue;
    }

    animalPrintGreeting(p);
    animalPrintMenu(p);
    free(p); 

    void* buffer = alloca(sizeof(Animal));
    Animal *stacked_p = (Animal*)myfactory(argv[1+2*i], argv[1+2*i+1], buffer);
    if (!stacked_p) {
      printf("Creation of stack-allocated plug-in object %s failed.\n", argv[1+2*i]);
      continue;
    }
    animalPrintGreeting(stacked_p);
    animalPrintMenu(stacked_p);
  }
}