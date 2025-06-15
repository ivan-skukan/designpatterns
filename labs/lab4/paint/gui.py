import tkinter as tk
from document_model import DocumentModel
from tkrenderer import TkRenderer
from line_segment import LineSegment
from oval import Oval
from point import Point
from idle_state import IdleState
from add_shape_state import AddShapeState
from select_shape_state import SelectShapeState


class GUI(tk.Frame):
  def __init__(self, root, objects):
    super().__init__(root)
    self.root = root
    self.pack(fill='both', expand=True)

    self.objects = objects  
    self.model = DocumentModel()

    self._currentState = IdleState()

    toolbar = tk.Frame(self)
    toolbar.pack(side='top', fill='x')

    for proto in self.objects:
      button = tk.Button(toolbar, text=proto.getShapeName(),
                         command=lambda p=proto: self.setState(AddShapeState(self.model, p)))
      button.pack(side='left')

    # manual adding for testing
    self.model.addGraphicalObject(LineSegment(Point(300, 300), Point(200, 200)))
    self.model.addGraphicalObject(Oval(Point(100, 100), Point(200, 200)))

    self.canvas = tk.Canvas(self, bg='white')
    self.canvas.pack(fill='both', expand=True)

    self.model.addDocumentModelListener(self)
    self.bind('<Configure>', lambda e: self.repaint())

    self.canvas.bind("<ButtonPress-1>", self._on_mouse_down)
    self.canvas.bind("<ButtonRelease-1>", self._on_mouse_up)
    self.canvas.bind("<B1-Motion>", self._on_mouse_dragged)
    self.canvas.bind("<KeyPress>", self._on_key_pressed)
    self.canvas.focus_set()

    self.repaint()

  def setState(self, newState):
    self._currentState.onLeaving()
    self._currentState = newState

  def repaint(self):
    self.canvas.delete("all")
    renderer = TkRenderer(self.canvas)
    for go in self.model.list():
      go.render(renderer)
      self._currentState.afterDraw(renderer, go)
    self._currentState.afterDraw(renderer)

  def document_change(self, model):
    self.repaint()

  def _on_mouse_down(self, event):
    self._currentState.mouseDown(Point(event.x, event.y), False, False)

  def _on_mouse_up(self, event):
    self._currentState.mouseUp(Point(event.x, event.y), False, False)

  def _on_mouse_dragged(self, event):
    self._currentState.mouseDragged(Point(event.x, event.y))

  def _on_key_pressed(self, event):
    if event.keysym == "Escape":
      self.setState(IdleState())
    else:
      self._currentState.keyPressed(event.keycode)
