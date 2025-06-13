import sys
sys.dont_write_bytecode = True

class Parrot:
  def __init__(self, name):
    self._name = name
  def name(self) -> str:
    return self._name
  def greet(self) -> str:
    return f"the Parrot squawks cheerfully!"
  def menu(self) -> str:
    return "colorful fruits and seeds"