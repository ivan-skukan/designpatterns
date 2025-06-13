import os
import importlib

def myfactory(moduleName):
  mymodule = importlib.import_module(f'plugins.{moduleName}')
  return getattr(mymodule, moduleName)

def printGreeting(pet):
  print(f'{pet.name()} says: {pet.greet()}')
def printMenu(pet):
  print(f'{pet.name()} eats: {pet.menu()}')

def test():
  pets=[]
  # obiđi svaku datoteku kazala plugins 
  for mymodule in os.listdir('plugins'):
    moduleName, moduleExt = os.path.splitext(mymodule)
    # ako se radi o datoteci s Pythonskim kodom ...
    if moduleExt=='.py':
      # instanciraj ljubimca ...
      ljubimac=myfactory(moduleName)('Ljubimac '+str(len(pets)))
      # ... i dodaj ga u listu ljubimaca
      pets.append(ljubimac)

  # ispiši ljubimce
  for pet in pets:
    printGreeting(pet)
    printMenu(pet)


if __name__ == '__main__':
  test()
  # import t12.plugins.parrot
  # p = t12.plugins.parrot.Parrot('Parrot')
  # print(p.name())
  # print(p.greet())
  # print(p.menu())
