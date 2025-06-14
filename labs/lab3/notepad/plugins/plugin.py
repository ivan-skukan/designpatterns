from abc import ABC, abstractmethod

class Plugin(ABC):
  @abstractmethod
  def getName(self) -> str:
    pass
  @abstractmethod
  def getDescription(self) -> str:
    pass
  @abstractmethod
  def execute(self, model, undoManager, clipboardStack):
    pass
