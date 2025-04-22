from abc import ABC, abstractmethod
import datetime, time
from statistics import mean, median

input_file = 'fifth_izvor.txt'
output_file = 'fifth_output.txt'

class Izvor(ABC):
  @abstractmethod
  def parsirajInput(self):
    pass

class Promatrac(ABC): 
  @abstractmethod
  def akcija(self,kolekcija):
    pass

class TipkovnickiIzvor(Izvor):
  def parsirajInput(self):
    return int(input('Your input: '))

class DatotecniIzvor(Izvor):
  def __init__(self,filename):
    self.filename = filename
    self.file = open(filename, 'r')

  def parsirajInput(self):
    inp = self.file.readline()
    if not inp:
      self.file.close()
      return -1
    return int(inp.strip())

class DatotekaPromatrac(Promatrac):
  def akcija(self,kolekcija):
    with open(output_file, 'a') as f:
      for elem in kolekcija:
        f.write(f'{elem},')
      f.write(f' {datetime.datetime.now()}\n')
      
class SumaPromatrac(Promatrac):
  def akcija(self,kolekcija):
    print('Suma: ', sum(kolekcija))

class ProsjekPromatrac(Promatrac):
  def akcija(self,kolekcija):
    print('Prosjek: ',mean(kolekcija))

class MedijanPromatrac(Promatrac):
  def akcija(self,kolekcija):
    print('Medijan: ',median(kolekcija))

class SlijedBrojeva:
  def __init__(self, izvor, promatraci):
    self.izvor = izvor
    self.kolekcija = []
    self.promatraci = promatraci

  def kreni(self):
    while True:
      time.sleep(1)
      inp = self.izvor.parsirajInput()
      if inp == -1:
        return
      else:
        self.kolekcija.append(inp)
      self.notify()

  def notify(self):
    for promatrac in self.promatraci:
      promatrac.akcija(self.kolekcija)

def main():
    choice = input("Choose input source (1 = keyboard, 2 = file): ").strip()
    if choice == "1":
        izvor = TipkovnickiIzvor()
    elif choice == "2":
        izvor = DatotecniIzvor(input_file)
    else:
        print("Invalid choice.")
        return

    promatraci = [
        DatotekaPromatrac(),
        SumaPromatrac(),
        ProsjekPromatrac(),
        MedijanPromatrac()
    ]

    slijed = SlijedBrojeva(izvor, promatraci)
    try:
        slijed.kreni()
    except KeyboardInterrupt:
        print("\nFin")

if __name__ == "__main__":
    main()
