from graphical_object import GraphicalObject
from rectangle import Rectangle
from point import Point
from typing import List


class CompositeShape(GraphicalObject):
  def __init__(self, children: List[GraphicalObject] = None):
    if children is None:
      children = []
    self.children = children
    self._selected = False
    self._listeners = []

  def isSelected(self) -> bool:
    return self._selected

  def setSelected(self, selected: bool):
    if self._selected != selected:
      self._selected = selected
      for child in self.children:
        child.setSelected(selected)
      self._notifyListeners()

  def getNumberOfHotPoints(self) -> int:
    return 0

  def getHotPoint(self, index: int) -> Point:
    raise IndexError("CompositeShape nema hot-pointove")

  def setHotPoint(self, index: int, point: Point):
    raise IndexError("CompositeShape nema hot-pointove")

  def isHotPointSelected(self, index: int) -> bool:
    raise IndexError("CompositeShape nema hot-pointove")

  def setHotPointSelected(self, index: int, selected: bool):
    raise IndexError("CompositeShape nema hot-pointove")

  def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
    raise IndexError("CompositeShape nema hot-pointove")

  def translate(self, delta: Point):
    for child in self.children:
      child.translate(delta)
    self._notifyListeners()

  def getBoundingBox(self) -> Rectangle:
    if not self.children:
      return Rectangle(0, 0, 0, 0)

    min_x = min(child.getBoundingBox().x for child in self.children)
    min_y = min(child.getBoundingBox().y for child in self.children)
    max_x = max(child.getBoundingBox().x + child.getBoundingBox().width for child in self.children)
    max_y = max(child.getBoundingBox().y + child.getBoundingBox().height for child in self.children)

    return Rectangle(min_x, min_y, max_x - min_x, max_y - min_y)

  def selectionDistance(self, mousePoint: Point) -> float:
    if not self.children:
      return float('inf')
    return min(child.selectionDistance(mousePoint) for child in self.children)

  def getShapeName(self) -> str:
    return "CompositeShape"

  def duplicate(self) -> GraphicalObject:
    duplicated_children = [child.duplicate() for child in self.children]
    return CompositeShape(duplicated_children)

  def addGraphicalObjectListener(self, l):
    if l not in self._listeners:
      self._listeners.append(l)
    for child in self.children:
      child.addGraphicalObjectListener(l)

  def removeGraphicalObjectListener(self, l):
    if l in self._listeners:
      self._listeners.remove(l)
    for child in self.children:
      child.removeGraphicalObjectListener(l)

  def _notifyListeners(self):
    for listener in self._listeners:
      listener.graphicalObjectChanged(self)

  def add(self, child: GraphicalObject):
    self.children.append(child)
    for listener in self._listeners:
      child.addGraphicalObjectListener(listener)
    self._notifyListeners()

  def remove(self, child: GraphicalObject):
    if child in self.children:
      self.children.remove(child)
      for listener in self._listeners:
        child.removeGraphicalObjectListener(listener)
      self._notifyListeners()
