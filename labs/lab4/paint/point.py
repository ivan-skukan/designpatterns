class Point:
  def __init__(self, x: int, y: int):
    self.x = x
    self.y = y

  def getX(self) -> int:
    return self.x

  def getY(self) -> int:
    return self.y

  def translate(self, dp: 'Point') -> 'Point':
    return Point(self.x + dp.getX(), self.y + dp.getY())

  def difference(self, p: 'Point') -> 'Point':
    return Point(self.x - p.getX(), self.y - p.getY())

  def __repr__(self):
    return f"Point({self.x}, {self.y})"