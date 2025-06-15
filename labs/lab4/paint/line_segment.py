from abstract_graphical_object import AbstractGraphicalObject
from graphical_object import GraphicalObject
from point import Point
from rectangle import Rectangle


class LineSegment(AbstractGraphicalObject):
  def __init__(self, start: Point = None, end: Point = None):
    if start is None:
      start = Point(0,0)
    if end is None:
      end = Point(10,0)
    super().__init__([start, end])

  def selectionDistance(self, mousePoint: Point) -> float:
    return GeometryUtil.distanceFromLineSegment(self._hot_points[0], self._hot_points[1], mousePoint)

  def getBoundingBox(self) -> Rectangle:
    xs = [p.x for p in self._hot_points]
    ys = [p.y for p in self._hot_points]
    x = min(xs)
    y = min(ys)
    width = max(xs) - x
    height = max(ys) - y
    return Rectangle(x, y, width, height)

  def duplicate(self) -> GraphicalObject:
    # copy hot points but do NOT copy listeners
    return LineSegment(Point(self._hot_points[0].x, self._hot_points[0].y),
                       Point(self._hot_points[1].x, self._hot_points[1].y))

  def getShapeName(self) -> str:
    return "Linija"

  def render(self, renderer):
    return renderer.drawLine(self._hot_points[0], self._hot_points[1])

  def copy(self) -> GraphicalObject:
    return self.duplicate()