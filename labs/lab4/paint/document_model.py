from graphical_object_listener import GraphicalObjectListener

class DocumentModel(GraphicalObjectListener):
  SELECTION_PROXIMITY = 10

  def __init__(self):
    self._objects = []
    self._listeners = []
    self._selected_objects = []

  def removeGraphicalObject(self, o):
    if o in self._objects:
      self._objects.remove(o)
      o.removeGraphicalObjectListener(self)
      self.notifyListeners()
      if o in self._selected_objects:
        self._selected_objects.remove(o)

  def clear(self):
    for o in self._objects[:]:
      self.removeGraphicalObject(o)    

  def addGraphicalObject(self, o):
    self._objects.append(o)
    o.addGraphicalObjectListener(self)
    self.notifyListeners()
    if o.isSelected():
      self._selected_objects.append(o)

  def list(self):
    return self._objects.copy()

  def addDocumentModelListener(self, l):
    if l not in self._listeners:
      self._listeners.append(l)

  def removeDocumentModelListener(self, l):
    if l in self._listeners:
      self._listeners.remove(l)

  def notifyListeners(self, txt=None):
    for l in self._listeners:
      l.document_change(self)
    print(f"DocumentModel: Notified listeners about change: {txt if txt else 'No specific change'}")


  def getSelectedObjects(self):
    return self._selected_objects.copy()

  def increaseZ(self, go):
    """Increase the Z-order of a graphical object by 1."""
    if go in self._objects:
      idx = self._objects.index(go)
      if idx < len(self._objects) - 1:
        self._objects[idx], self._objects[idx + 1] = self._objects[idx + 1], self._objects[idx]
        self.notifyListeners()

  def decreaseZ(self, go):
    """Decrease the Z-order of a graphical object by 1."""
    if go in self._objects:
      idx = self._objects.index(go)
      if idx > 0:
        self._objects[idx], self._objects[idx - 1] = self._objects[idx - 1], self._objects[idx]
        self.notifyListeners()

  def findSelectedGraphicalObject(self, point):
    closest_obj, min_distance = None, float('inf')
    for o in self._objects:
      d = o.selectionDistance(point)
      if d < self.SELECTION_PROXIMITY and (closest_obj is None or d < min_distance):
        closest_obj, min_distance = o, d
    return closest_obj

  def graphicalObjectChanged(self, go):
    """Called when a graphical object has changed (e.g., hot-point moved, selection changed)."""
    self.notifyListeners()

  def graphicalObjectSelectionChanged(self, go): # not sure
    """Called when the selection state of a graphical object has changed."""
    if go.isSelected():
      if go not in self._selected_objects:
        self._selected_objects.append(go)
    else:
      if go in self._selected_objects:
        self._selected_objects.remove(go)
    self.notifyListeners()
  