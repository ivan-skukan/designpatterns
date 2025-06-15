from state import State

class AddShapeState(State):
  def __init__(self, model, prototype):
    self.model = model
    self.prototype = prototype

  def mouseDown(self, mousePoint, shiftDown, ctrlDown):
    go = self.prototype.copy()
    go.translate(mousePoint)
    self.model.addGraphicalObject(go)

  def mouseUp(self, mousePoint, shiftDown, ctrlDown):
    pass

  def mouseDragged(self, mousePoint):
    pass

  def keyPressed(self, keyCode):
    pass

  def afterDraw(self, renderer, go=None):
    pass

  def onLeaving(self):
    pass
