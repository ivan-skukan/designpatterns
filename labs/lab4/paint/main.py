import tkinter as tk
from gui import GUI
from line_segment import LineSegment
from oval import Oval

if __name__ == "__main__":
  root = tk.Tk()
  root.geometry("600x400")
  objects = [LineSegment(), Oval()]
  gui = GUI(root, objects)
  root.mainloop()
