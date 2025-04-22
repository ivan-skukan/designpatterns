import re

class Cell:
  def __init__(self, sheet):
    self.sheet = sheet
    self.exp = None
    self.value = None
    self.listeners = []

  def add_listener(self, listener):
    if listener not in self.listeners:
      self.listeners.append(listener)

  def notify_listeners(self):
    for listener in self.listeners:
      listener.set_value(None)  
      listener.evaluate()

  def set_value(self, value):
    if self.value != value:
      self.value = value
      self.notify_listeners()

  def evaluate(self, visited=None):
    if visited is None:
      visited = set()
    if self in visited:
      raise RuntimeError(f"Cyclic dependency detected involving {self.exp}")
    visited.add(self)

    if self.exp is None:
      self.set_value(0)
      return self.value

    if self.exp.isdigit():
      self.set_value(int(self.exp))
      return self.value

    if self.value:
      return self.value

    refs = self.sheet.getrefs(self)
    value = 0
    for ref_cell in refs:
      value += ref_cell.evaluate(visited)
    self.set_value(value)
    return value


class Sheet:
  def __init__(self, rows, cols):
    self.cells = []
    for i in range(rows):
      row = []
      for j in range(cols):
        row.append(Cell(self))
      self.cells.append(row)
    self.rows = rows
    self.cols = cols

  def cell(self, ref):
    match = re.match(r'([A-Z]+)([0-9]+)', ref)
    col_str, row_str = match.groups()
    col = sum((ord(char) - ord('A') + 1) * (26 ** (len(col_str) - idx - 1)) for idx, char in enumerate(col_str)) - 1
    """ 
    AAB
    idx = 0, char = 'A' → (1) * 26^(2) = 1 * 676 = 676
    idx = 1, char = 'A' → (1) * 26^(1) = 1 * 26  = 26
    idx = 2, char = 'B' → (2) * 26^(0) = 2 * 1   = 2
    676 + 26 + 2 = 704
    """
    row = int(row_str) - 1
    return self.cells[row][col]

  def set(self, ref, exp):
    cell = self.cell(ref)
    self.clear_references(cell)
    cell.exp = exp
    cell.value = None
    refs = self.getrefs(cell)
    for ref_cell in refs:
      ref_cell.add_listener(cell)
    self.evaluate(cell)

  def getrefs(self, cell):
    refs = re.findall(r'[A-Z]+\d+', cell.exp or '')
    return [self.cell(ref) for ref in refs]

  def clear_references(self, cell):
    for row in self.cells:
      for c in row:
        if cell in c.listeners:
          c.listeners.remove(cell)

  def evaluate(self, cell):
    return cell.evaluate()

  def print(self):
    for i in range(self.rows):
      for j in range(self.cols):
        cell = self.cells[i][j]
        value = cell.value if cell.value is not None else 'N/A'
        print(f'({i+1},{j+1}): {value}', end='  ')
      print()

if __name__ == "__main__":
  s = Sheet(5, 5)
  s.set('A1', '2')
  s.set('A2', '5')
  s.set('A3', 'A1+A2')
  s.print()
  print()
  print()
  s.set('A1', '4')
  s.print()
  print()
  print()
  s.set('A4', 'A1+A3')
  s.print()
  print()
  print()

  try:
    s.set('A1', 'A3')
  except RuntimeError as e:
    print("Caught exception:", e)
  s.print()
