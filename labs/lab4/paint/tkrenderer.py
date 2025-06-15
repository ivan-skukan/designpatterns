from renderer import Renderer
import tkinter as tk


class TkRenderer(Renderer):
    def __init__(self, canvas):
        super().__init__()
        self.canvas = canvas

    def drawLine(self, s, e, color='black'):
        self.canvas.create_line(s.x, s.y, e.x, e.y, fill=color)

    def fillPolygon(self, points):
        points_list = [(p.x, p.y) for p in points]
        self.canvas.create_polygon(points_list, fill='purple', outline='black')

    def drawOval(self, boundingBox, color='black'):
        x0 = boundingBox.x
        y0 = boundingBox.y
        x1 = boundingBox.x + boundingBox.width
        y1 = boundingBox.y + boundingBox.height
        self.canvas.create_oval(x0, y0, x1, y1, outline=color)

    def drawPoint(self, point, size=2, color='black'):
        x = point.x
        y = point.y
        self.canvas.create_oval(x - size, y - size, x + size, y + size, fill=color, outline=color)