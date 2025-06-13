#include  "myfactory.h"
#include <stdio.h>
#include <dlfcn.h>
#include <stdlib.h>


typedef void* (*PTRFUN)(char const*);
typedef void (*CONSTRUCT_PTRFUN)(void*, char const*);
typedef size_t (*SIZEOF_PTRFUN)();

void* myfactory(char const* libname, char const* ctorarg, void* buffer) {
  char path[256];
  snprintf(path, sizeof(path), "./%s.so", libname);

  void* handle = dlopen(path, RTLD_LAZY);
  if (!handle) {
    fprintf(stderr, "dlopen error: %s\n", dlerror());
    return NULL;
  }

  dlerror(); //clear existing errors
  SIZEOF_PTRFUN sizeof_fun = (SIZEOF_PTRFUN) dlsym(handle, "sizeof_");
  CONSTRUCT_PTRFUN construct_fun = (CONSTRUCT_PTRFUN) dlsym(handle, "construct");
  PTRFUN create_fun = (PTRFUN) dlsym(handle, "create");
  char* error = dlerror();
  if (error) {
    fprintf(stderr, "dlsym error: %s\n", error);
    dlclose(handle); // unnecessary?
    return NULL;
  }

  void* buff2;

  if (buffer == NULL) {
    size_t size = sizeof_fun();
    buff2 = malloc(size);
    if (!buff2) {
      fprintf(stderr, "Memory allocation failed\n");
      dlclose(handle);
      return NULL;
    }
  } else {
    buff2 = buffer;
  }
  construct_fun(buff2, ctorarg);

  return buff2;
}

