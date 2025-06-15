from abc import ABC, abstractmethod


class GraphicalObjectListener(ABC):
  @abstractmethod
  def graphicalObjectChanged(self, go: 'GraphicalObject'): 
    """Called when a graphical object has changed (e.g., hot-point moved, selection changed)."""
    pass
  def graphicalObjectSelectionChanged(self, go: 'GraphicalObject'): 
    """Called when the selection state of a graphical object has changed."""
    pass