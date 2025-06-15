import math
from point import Point

class GeometryUtil:
  @staticmethod
  def distanceFromPoint(p1: Point, p2: Point) -> float:
    dx = p1.x - p2.x
    dy = p1.y - p2.y
    return math.sqrt(dx*dx + dy*dy)

  @staticmethod
  def distanceFromLineSegment(s: Point, e: Point, p: Point) -> float:
    len_sq = (e.x - s.x) ** 2 + (e.y - s.y) ** 2

    if len_sq == 0:
      return GeometryUtil.distanceFromPoint(s, p)
      
    t = ((p.x - s.x) * (e.x - s.x) + (p.y - s.y) * (e.y - s.y)) / len_sq
    t = max(0, min(1, t)) 
    
    closest = Point(s.x + t * (e.x - s.x), s.y + t * (e.y - s.y))
    
    return GeometryUtil.distanceFromPoint(p, closest)  
