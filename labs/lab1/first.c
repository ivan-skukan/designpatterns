#include <stdio.h>
#include <stdlib.h>
#include <string.h>


typedef char const* (*PTRFUN)(); //?

typedef struct {
  PTRFUN greet;
  PTRFUN menu;
} vtable;

typedef struct {
  char* name;
  vtable* vtable; //? Kasnije castamo type na potrebnu tablicu?
} Animal;

void animalPrintGreeting(Animal* p) {
  printf("%s pozdravlja: %s\n", p->name, p->vtable->greet());
}
void animalPrintMenu(Animal* p) {
  printf("%s voli %s\n", p->name, p->vtable->menu()); // check
}

char const* dogGreet(void){
    return "vau!";
}
char const* dogMenu(void){
  return "kuhanu govedinu";
}
char const* catGreet(void){
  return "mijau!";
}
char const* catMenu(void){
  return "konzerviranu tunjevinu";
}

vtable cat_table = {
  .greet = catGreet,
  .menu = catMenu
};
vtable dog_table = {
  .greet = dogGreet,
  .menu = dogMenu
}; // should these be created globally

void constructCat(char const* name, Animal* cat) {
  cat->name = (char*)malloc(strlen(name)+1);
  strcpy(cat->name,name); //check all 
  cat->vtable = &cat_table;
}

void constructDog(char const* name, Animal* dog) { //check
  dog->name = (char*)malloc(strlen(name)+1);
  strcpy(dog->name,name); //check all 
  dog->vtable = &dog_table;
}

Animal* createCat(char const* name) {
  Animal* cat = (Animal*)malloc(sizeof(Animal));
  constructCat(name, cat);
  return cat;
}

Animal* createDog(char const* name) {
  Animal* dog = (Animal*)malloc(sizeof(Animal));
  constructDog(name, dog);
  return dog;
}

void createNDogs(int n) {
  Animal** dogs = (Animal**)malloc(sizeof(Animal*) * n); // check
  for (int i = 0; i < n; i++) {
    char name[20];
    snprintf(name, sizeof(name), "Dog%d", i);
    dogs[i] = createDog(name);
  }

  for (int i = 0; i < n; i++) {
    animalPrintGreeting(dogs[i]);
    free(dogs[i]->name);
    free(dogs[i]);
  }
  free(dogs);
}

void testAnimals(void){
  Animal* p1=createDog("Hamlet");
  Animal* p2=createCat("Ofelija");
  Animal* p3=createDog("Polonije");

  animalPrintGreeting(p1);
  animalPrintGreeting(p2);
  animalPrintGreeting(p3);

  animalPrintMenu(p1);
  animalPrintMenu(p2);
  animalPrintMenu(p3);

  createNDogs(4);

  free(p1->name); free(p2->name); free(p3->name);
  free(p1); free(p2); free(p3);
}

void stackCreate(void) {
  Animal dog;
  dog.name = "doggo";
  dog.vtable = &dog_table; // just call construct?

  printf("Name: %s\n", dog.name);
  printf("menu: %s\n", dog.vtable->menu());
}

int main(int argc, char** argv) {
  testAnimals();
  stackCreate();

  return 0;
}