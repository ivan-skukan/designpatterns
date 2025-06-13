#ifndef ANIMAL_H
#define ANIMAL_H


typedef struct {
  char const* (*vtable[3])();
  char const* name;
} Animal;

void animalPrintGreeting(void* p);
void animalPrintMenu(void* p);


#endif // ANIMAL_H