from typing import Callable
from graphical_object import GraphicalObject
from graphical_object_listener import GraphicalObjectListener
from typing import List
from point import Point
from rectangle import Rectangle
from abc import abstractmethod


class AbstractGraphicalObject(GraphicalObject):
  def __init__(self, hot_points: List[Point]):
    self._hot_points = hot_points
    self._hot_point_selected = [False] * len(hot_points)
    self._selected = False
    self._listeners: List[GraphicalObjectListener] = []

  # Selection status
  def isSelected(self) -> bool:
    return self._selected

  def setSelected(self, selected: bool):
    if self._selected != selected:
      self._selected = selected
      self._notifySelectionChanged()

  # Hot-point management
  def getNumberOfHotPoints(self) -> int:
    return len(self._hot_points)

  def getHotPoint(self, index: int) -> Point:
    return self._hot_points[index]

  def setHotPoint(self, index: int, point: Point):
    self._hot_points[index] = point
    self._notifyChanged()

  def isHotPointSelected(self, index: int) -> bool:
    return self._hot_point_selected[index]

  def setHotPointSelected(self, index: int, selected: bool):
    self._hot_point_selected[index] = selected
    self._notifyChanged()

  def getHotPointDistance(self, index: int, mousePoint: Point) -> float:
    return GeometryUtil.distanceFromPoint(self._hot_points[index], mousePoint)

  def translate(self, delta: Point):
    self._hot_points = [hp.translate(delta) for hp in self._hot_points]
    self._notifyChanged()

  def addGraphicalObjectListener(self, l: GraphicalObjectListener):
    if l not in self._listeners:
      self._listeners.append(l)

  def removeGraphicalObjectListener(self, l: GraphicalObjectListener):
    if l in self._listeners:
      self._listeners.remove(l)

  def _notifyChanged(self):
    for l in self._listeners:
      l.graphicalObjectChanged(self)

  def _notifySelectionChanged(self):
    for l in self._listeners:
      l.graphicalObjectSelectionChanged(self)

  # Abstract methods to be implemented by subclasses
  @abstractmethod
  def selectionDistance(self, mousePoint: Point) -> float:
    pass

  @abstractmethod
  def getBoundingBox(self) -> Rectangle:
    pass

  @abstractmethod
  def duplicate(self) -> 'GraphicalObject':
    pass

  @abstractmethod
  def getShapeName(self) -> str:
    pass
