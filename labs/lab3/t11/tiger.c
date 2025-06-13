#include <stdio.h>
#include <stdlib.h>


typedef char const* (*PTRFUN)();

typedef struct {
  PTRFUN* vtable;
  char const* name;
} Tiger;

char const* name(void* this) {
  Tiger* t = (Tiger*)this;
  return t->name;
}

char const* greet() {
  return "Tigar";
}

char const* menu() {
  return "Jelen i antilopa";
}

PTRFUN vtable_Tiger[3] = {name, greet, menu};

size_t sizeof_() {
  return sizeof(Tiger);
}

void construct(void* p, char const* name) {
  Tiger* t = (Tiger*)p;
  t->name = name;
  t->vtable = vtable_Tiger;
}

Tiger* create(char const* name){
  Tiger* t = (Tiger*)malloc(sizeof(Tiger));
  if (!t) {
    return NULL; 
  }
  construct(t, name);
  return t;
}