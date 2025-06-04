from editaction import EditAction

class UndoObserver:
  def updateUndoRedoStatus(self, can_undo: bool, can_redo: bool):
    pass


class UndoManager:
  _instance = None

  def __init__(self):
    if UndoManager._instance is not None:
      raise Exception("Use UndoManager.get_instance() instead")
    self.undoStack = []
    self.redoStack = []
    self._observers = []

  @staticmethod
  def get_instance():
    if UndoManager._instance is None:
      UndoManager._instance = UndoManager()
    return UndoManager._instance

  def addObserver(self, observer: UndoObserver):
    self._observers.append(observer)

  def removeObserver(self, observer: UndoObserver):
    self._observers.remove(observer)

  def notifyObservers(self):
    for obs in self._observers:
      obs.updateUndoRedoStatus(bool(self.undoStack), bool(self.redoStack))

  def push(self, action: EditAction):
    self.undoStack.append(action)
    self.redoStack.clear()
    self.notifyObservers()

  def undo(self):
    if not self.undoStack:
      return
    action = self.undoStack.pop()
    action.execute_undo()
    self.redoStack.append(action)
    self.notifyObservers()

  def redo(self):
    if not self.redoStack:
      return
    action = self.redoStack.pop()
    action.execute_do()
    self.undoStack.append(action)
    self.notifyObservers()
