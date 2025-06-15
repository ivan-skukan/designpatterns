from abc import ABC, abstractmethod
from typing import List

class Renderer(ABC):
  @abstractmethod
  def drawLine(self, s: 'Point', e: 'Point'):
    """Draw a line from point s to point e."""
    pass
  def fillPolygon(self, points: List['Point']):
    """Fill a polygon defined by the list of points."""
    pass
  @abstractmethod
  def drawOval(self, bb):
    """Draw an oval defined by the bounding box."""
    pass
  @abstractmethod
  def drawPoint(self, p: 'Point'):
    """Draw a point."""
    pass