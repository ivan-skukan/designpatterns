import tkinter as tk
from texteditormodel import TextEditorModel
import tkinter.font as tkfont
from cursorobserver import CursorObserver
from textobserver import TextObserver
from location import Location
from locationrange import LocationRange
from clipboardstack import ClipboardStack, ClipboardObserver

font_size = 10

class TextEditor(tk.Canvas, CursorObserver, TextObserver, ClipboardObserver):
  def __init__(self, root, tem: TextEditorModel=None, **kwargs):
    super().__init__(root, **kwargs)
    self.root = root
    self._tem = tem
    self._clipboardStack = ClipboardStack()

    self.font = tkfont.Font(family='Courier', size=font_size)
    self.char_width = self.font.measure('A')

    self.focus_set() 
    self.set_binds()
    self._tem.subscribe_cursorObserver(self) 
    self._tem.subscribe_textObserver(self)
    self._clipboardStack.add_observer(self)
    self.updateDisplay()

  def set_binds(self):
    self.bind('<Key>', self.handle_key_press)
    self.focus_set()

  def handle_key_press(self, event):
    shift_held = (event.state & 0x0001) != 0
    ctrl_held = (event.state & 0x0004) != 0

    old_cursor = Location(self._tem.cursorLocation.row, self._tem.cursorLocation.column)
    moved = False

    if ctrl_held:
      if event.keysym.lower() == 'c':  # CTRL+C
        selection = self._tem.getSelectionRange()
        if selection:
          text = self._tem.getSelectedText(selection)
          if text:
            self._clipboardStack.push(text)
        return

      elif event.keysym.lower() == 'x':  # CTRL+X
        selection = self._tem.getSelectionRange()
        if selection:
          text = self._tem.getSelectedText(selection)
          if text:
            self._clipboardStack.push(text)
            self._tem.deleteRange(selection)
            self._tem.setSelectionRange(None)
        return

      elif event.keysym.lower() == 'v':  # CTRL+V or CTRL+SHIFT+V
        clip_text = None
        if shift_held:
          clip_text = self._clipboardStack.pop()
        else:
          clip_text = self._clipboardStack.peek()
        if clip_text:
          if self._tem.getSelectionRange():
            self._tem.deleteRange(self._tem.getSelectionRange())
            self._tem.setSelectionRange(None)
          self._tem.insert(clip_text)
        return
      
      elif event.keysym.lower() == 'z':
        self._tem.undoManager.undo()
        return
      elif event.keysym.lower() == 'y':
        self._tem.undoManager.redo()


    # Not CTRL combos — normal movement or insertion

    if event.keysym == 'Left':
        moved = self._tem.moveCursorLeft()
    elif event.keysym == 'Right':
        moved = self._tem.moveCursorRight()
    elif event.keysym == 'Up':
        moved = self._tem.moveCursorUp()
    elif event.keysym == 'Down':
        moved = self._tem.moveCursorDown()
    elif (event.char and ord(event.char) >= 32) or event.keysym == 'Return':
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      self._tem.insert(event.char)
    elif event.keysym == 'BackSpace':
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      else:
        self._tem.deleteBefore()
    elif event.keysym == 'Delete':
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      else:
        self._tem.deleteAfter()

    if moved:
      new_cursor = self._tem.cursorLocation
      if shift_held:
        if not self._tem.getSelectionRange():
          self._tem.setSelectionRange(LocationRange(old_cursor, new_cursor))
        else:
          start = self._tem.getSelectionRange().locationStart
          self._tem.setSelectionRange(LocationRange(start, new_cursor))
      else:
        if self._tem.getSelectionRange():
          self._tem.setSelectionRange(None)




  def updateDisplay(self):
    self.updateText()
    self.updateCursorLocation() # is this good?
    
  def updateText(self):
    self.delete('text')
    self.delete('selection')

    selection = self._tem.getSelectionRange()
    for row, line in enumerate(self._tem.allLines()):
      if selection:
        # Normalize start and end
        start, end = selection.locationStart, selection.locationEnd
        if (start.row > end.row) or (start.row == end.row and start.column > end.column):
          start, end = end, start

        if start.row <= row <= end.row:
          start_col = 0
          end_col = len(line)
          if row == start.row:
            start_col = start.column
          if row == end.row:
            end_col = end.column

          x1 = start_col * self.char_width
          x2 = end_col * self.char_width
          y = row * (font_size + 5)

          self.create_rectangle(x1, y, x2, y + font_size + 2, fill='lightblue', tags='selection')

      self.create_text(0, row*(font_size+5), text=line, font=self.font, anchor='nw', tags='text')

  def updateCursorLocation(self, loc: Location = Location(0,0)):
    self.delete('cursor')
    row, column = loc.row, loc.column
    self.create_line(1+self.char_width*column,(row*(font_size+5)),1+self.char_width*column,(row*(font_size+5)+font_size), fill='black', width=3, tags='cursor')

  def updateClipboard(self):
    #useless
    pass
