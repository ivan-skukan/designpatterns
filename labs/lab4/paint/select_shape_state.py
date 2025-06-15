from state import State
from point import Point
from geometry_util import GeometryUtil
from document_model import DocumentModel

class SelectShapeState(State):
  def __init__(self, model):
    self.model = model
    self.selected_objects = []
    self.dragging_object = None
    self.dragging_hotpoint_index = None

  def mouseDown(self, mousePoint, shiftDown, ctrlDown):
    PROXIMITY = DocumentModel.SELECTION_PROXIMITY

    if len(self.selected_objects) == 1:
      clicked_object = self.selected_objects[0]
      for i in range(clicked_object.getNumberOfHotPoints()):
        hp = clicked_object.getHotPoint(i)
        if GeometryUtil.distanceFromPoint(hp, mousePoint) <= PROXIMITY:
          self.dragging_object = clicked_object
          self.dragging_hotpoint_index = i
          clicked_object.setHotPointSelected(i, True)
          return

    clicked_object = self.model.findSelectedGraphicalObject(mousePoint)

    if clicked_object:
      if ctrlDown:
        if clicked_object in self.selected_objects:
          self.selected_objects.remove(clicked_object)
        else:
          self.selected_objects.append(clicked_object)
      else:
        self.selected_objects = [clicked_object]
      self.model.notifyListeners(clicked_object.getShapeName())
    else:
      if not ctrlDown:
        self.selected_objects.clear()
        self.model.notifyListeners(None)

  def mouseDragged(self, mousePoint):
    if self.dragging_object and self.dragging_hotpoint_index is not None:
      self.dragging_object.setHotPoint(self.dragging_hotpoint_index, mousePoint)
      self.model.notifyListeners()

  def mouseUp(self, mousePoint):
    if self.dragging_object and self.dragging_hotpoint_index is not None:
      self.dragging_object.setHotPointSelected(self.dragging_hotpoint_index, False)

    self.dragging_object = None
    self.dragging_hotpoint_index = None

  def keyPressed(self, keyCode):
    if not self.selected_objects:
      return

    dx, dy = 0, 0
    if keyCode == 37:   # left
      dx = -1
    elif keyCode == 38: # up
      dy = -1
    elif keyCode == 39: # right
      dx = 1
    elif keyCode == 40: # down
      dy = 1

    if dx != 0 or dy != 0:
      for go in self.selected_objects:
        go.translate(Point(dx, dy))

    if keyCode == 43: # '+'
      for go in self.selected_objects:
        self.model.increaseZ(go)
    elif keyCode == 45: # '-'
      for go in self.selected_objects:
        self.model.decreaseZ(go)

    self.model.notifyListeners()

  def afterDraw(self, renderer, go=None):
    if go is not None and go in self.selected_objects:
      # Draw bounding box
      rect = go.getBoundingBox()
      points = [
        Point(rect.x, rect.y),
        Point(rect.x + rect.width, rect.y),
        Point(rect.x + rect.width, rect.y + rect.height),
        Point(rect.x, rect.y + rect.height)
      ]
      for i in range(4):
        renderer.drawLine(points[i], points[(i + 1) % 4])

      if len(self.selected_objects) == 1:
        for i in range(go.getNumberOfHotPoints()):
          hp = go.getHotPoint(i)
          size = 3
          renderer.fillPolygon([
            Point(hp.x - size, hp.y - size),
            Point(hp.x + size, hp.y - size),
            Point(hp.x + size, hp.y + size),
            Point(hp.x - size, hp.y + size)
          ])

  def onLeaving(self):
    self.selected_objects.clear()
    self.dragging_object = None
    self.dragging_hotpoint_index = None
    self.model.notifyListeners()
