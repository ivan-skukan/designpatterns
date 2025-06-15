from geometry_util import GeometryUtil
from abstract_graphical_object import AbstractGraphicalObject
from point import Point
from rectangle import Rectangle
from graphical_object import GraphicalObject


class Oval(AbstractGraphicalObject):
  def __init__(self, right_hot_point: Point = None, bottom_hot_point: Point = None):
    if right_hot_point is None:
      right_hot_point = Point(10, 0)
    if bottom_hot_point is None:
      bottom_hot_point = Point(0, 10)
    super().__init__([right_hot_point, bottom_hot_point])

  def selectionDistance(self, mousePoint: Point) -> float:
    return GeometryUtil.distanceFromLineSegment(self.right_hot_point, self.bottom_hot_point, mousePoint)
  def getBoundingBox(self) -> Rectangle:
    minx = min(self._hot_points[0].x, self._hot_points[1].x)
    miny = min(self._hot_points[0].y, self._hot_points[1].y)
    maxx = max(self._hot_points[0].x, self._hot_points[1].x)
    maxy = max(self._hot_points[0].y, self._hot_points[1].y)
    width = maxx - minx
    height = maxy - miny
    return Rectangle(minx, miny, 2*width, 2*height)
  def duplicate(self) -> GraphicalObject:
    return Oval(self.right_hot_point, self.bottom_hot_point)
  def getShapeName(self) -> str:
    return "Oval"

  def render(self, renderer):
    bounding_box = (self.getBoundingBox())
    renderer.drawOval(bounding_box, color='purple')

  def copy(self):
    return Oval(self._hot_points[0], self._hot_points[1])
