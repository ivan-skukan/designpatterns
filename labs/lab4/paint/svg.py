from renderer import Renderer


class SVGRendererImpl(Renderer):
  def __init__(self, file_name):
    self.file_name = file_name
    self.lines = []
    self.lines.append('<svg xmlns="http://www.w3.org/2000/svg" version="1.1">')

  def close(self):
    self.lines.append('</svg>')
    with open(self.file_name, 'w') as file:
      file.write('\n'.join(self.lines))

  def drawLine(self, s, e):
    line = f'<line x1="{s.x}" y1="{s.y}" x2="{e.x}" y2="{e.y}" stroke="black" />'
    self.lines.append(line)

  def fillPolygon(self, points):
    point_str = ' '.join(f'{p.x},{p.y}' for p in points)
    polygon = f'<polygon points="{point_str}" style="stroke:black; fill:gray; fill-opacity:0.4;" />'
    self.lines.append(polygon)

  def drawOval(self, bounding_box, color='purple'):
    x,y,width,height = bounding_box.x, bounding_box.y, bounding_box.width, bounding_box.height
    cx = x + width / 2
    cy = y + height / 2
    rx = width / 2
    ry = height / 2

    oval = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" style="stroke:black; fill:{color}; fill-opacity:0.3;" />'
    self.lines.append(oval)

  def drawPoint(self, point, size=3, color='red'):
    circle = f'<circle cx="{point.x}" cy="{point.y}" r="{size}" fill="{color}" />'
    self.lines.append(circle)
