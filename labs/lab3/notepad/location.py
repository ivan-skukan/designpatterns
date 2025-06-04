class Location:
  def __init__(self, row, column):
    self.row = row
    self.column = column
  def copy(self):
    return Location(self.row, self.column)