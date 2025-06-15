from point import Point

class SelectShapeState:
  def __init__(self, model):
    self.model = model
    self.selected_objects = []
    self.dragging = False
    self.drag_hot_point_index = None
    self.drag_start_point = None

  def mouseDown(self, mousePoint, shiftDown, ctrlDown):
    obj = self.model.findSelectedGraphicalObject(mousePoint)
    if obj:
      if ctrlDown:
        # dodaj u selekciju
        if obj not in self.selected_objects:
          self.selected_objects.append(obj)
          obj.setselected(True)
      else:
        # bez ctrl - selektiraj samo taj objekt
        for o in self.selected_objects:
          o.setselected(False)
        self.selected_objects = [obj]
        obj.setselected(True)

      # Ako je točno jedan objekt selektiran, provjeri hot-point
      if len(self.selected_objects) == 1:
        go = self.selected_objects[0]
        # Pretpostavimo da imaš metodu koja vraća indeks hot-pointa ako je kliknut blizu njega
        self.drag_hot_point_index = go.hotPointIndexAt(mousePoint)
        if self.drag_hot_point_index is not None:
          self.dragging = True
          self.drag_start_point = mousePoint
    else:
      # Kliknuto prazno, odselektiraj sve
      for o in self.selected_objects:
        o.setselected(False)
      self.selected_objects = []

    self.model.notifyListeners()

  def mouseUp(self, mousePoint, shiftDown, ctrlDown):
    self.dragging = False
    self.drag_hot_point_index = None

  def mouseDragged(self, mousePoint):
    if self.dragging and len(self.selected_objects) == 1:
      go = self.selected_objects[0]
      go.setHotPoint(self.drag_hot_point_index, mousePoint)
      self.model.graphicalObjectChanged(go)

  def keyPressed(self, keyCode):
    if not self.selected_objects:
      return
    if keyCode in (37, 38, 39, 40):
      dx = dy = 0
      if keyCode == 37: dx = -1
      if keyCode == 39: dx = 1
      if keyCode == 38: dy = -1
      if keyCode == 40: dy = 1
      for o in self.selected_objects:
        o.translate(dx, dy)
        self.model.graphicalObjectChanged(o)
    elif keyCode == 43:  # '+'
      for o in self.selected_objects:
        self.model.increaseZ(o)
    elif keyCode == 45:  # '-'
      for o in self.selected_objects:
        self.model.decreaseZ(o)

  def afterDraw(self, r, go=None):
    if go is not None:
      if go in self.selected_objects:
        bbox = go.boundingBox() 
        x0, y0, x1, y1 = bbox
        r.drawRect(x0, y0, x1, y1, color='blue')

        if len(self.selected_objects) == 1:
          go.drawHotPoints(r)
    else:
      pass

  def onLeaving(self):
    # deselect sve
    for o in self.selected_objects:
      o.setselected(False)
    self.selected_objects = []
    self.model.notifyListeners()
