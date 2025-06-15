from abc import ABC, abstractmethod
from point import Point

class GraphicalObject(ABC):
  
  @abstractmethod
  def isSelected(self) -> bool: ...
  
  @abstractmethod
  def setSelected(self, selected: bool): ...
  
  @abstractmethod
  def getNumberOfHotPoints(self) -> int: ...
  
  @abstractmethod
  def getHotPoint(self, index: int) -> 'Point': ...
  
  @abstractmethod
  def setHotPoint(self, index: int, point: 'Point'): ...
  
  @abstractmethod
  def isHotPointSelected(self, index: int) -> bool: ...
  
  @abstractmethod
  def setHotPointSelected(self, index: int, selected: bool): ...
  
  @abstractmethod
  def getHotPointDistance(self, index: int, mousePoint: 'Point') -> float: ...
  
  @abstractmethod
  def translate(self, delta: 'Point'): ...
  
  @abstractmethod
  def getBoundingBox(self) -> 'Rectangle': ...
  
  @abstractmethod
  def selectionDistance(self, mousePoint: 'Point') -> float: ...
  
  @abstractmethod
  def getShapeName(self) -> str: ...
  
  @abstractmethod
  def duplicate(self) -> 'GraphicalObject': ...
  
  @abstractmethod
  def addGraphicalObjectListener(self, l): ...
  
  @abstractmethod
  def removeGraphicalObjectListener(self, l): ...

  #  @abstractmethod
  #  def getShapeID(self) -> str:
  #    """Get the identifier of the shape"""
  #    raise NotImplementedError

  #  @abstractmethod
  #  def load(self, stack: List['GraphicalObject'], data: str) -> None:
  #    """Load the graphical object from data"""
  #    raise NotImplementedError

  #  @abstractmethod
  #  def save(self, rows: List[str]) -> None:
  #    """Save the graphical object to rows"""
  #    raise NotImplementedError