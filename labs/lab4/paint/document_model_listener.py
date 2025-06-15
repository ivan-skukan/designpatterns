from abc import ABC, abstractmethod

class DocumentModelListener(ABC):
  @abstractmethod
  def document_change(self) -> None:
    """Called when the document changes."""
    pass