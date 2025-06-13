import sys
sys.dont_write_bytecode = True

class Tiger:
  def __init__(self, name):
    self._name = name
  def name(self) -> str:
    return self._name
  def greet(self) -> str:
    return f"the Tiger roars majestically!"
  def menu(self) -> str:
    return "delicious humans"