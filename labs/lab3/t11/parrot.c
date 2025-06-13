#include <stdio.h>
#include <stdlib.h>


typedef char const* (*PTRFUN)();

typedef struct {
  PTRFUN* vtable;
  char const* name;
} Parrot;

char const* name(void* this) {
  Parrot* p = (Parrot*)this;
  return p->name;
}

char const* greet() {
  return "Papiga";
}

char const* menu() {
  return "kaj god papige jedu";
}

PTRFUN vtable_parrot[3] = {name, greet, menu};

size_t sizeof_() {
  return sizeof(Parrot);
}

void construct(void* pp, char const* name) {
  Parrot* p = (Parrot*)pp;
  p->name = name;
  p->vtable = vtable_parrot;
}

Parrot* create(char const* name_){
  Parrot* p = (Parrot*)malloc(sizeof(Parrot));
  if (!p) {
    return NULL; 
  }
  p->name = name_;
  p->vtable = vtable_parrot;
  return p;
}


