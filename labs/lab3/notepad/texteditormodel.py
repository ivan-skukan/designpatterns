import tkinter as tk
from location import Location
from locationrange import LocationRange
from cursorobserver import CursorObserver
from textobserver import TextObserver
from undomanager import UndoManager
from editaction import InsertAction, DeleteAction

class TextEditorModel:
  def __init__(self, text=''):
    self.lines = [line for line in text.split('\n')]
    self._selectionRange: LocationRange = None
    self.cursorLocation: Location = Location(0,0)

    self._cursorObservers = []
    self._textObservers = []

    self.undoManager = UndoManager.get_instance()

  def allLines(self):
    return iter(self.lines)

  def linesRange(self, idx1, idx2):
    return iter(self.lines[idx1:idx2])

  def subscribe_cursorObserver(self, observer: CursorObserver):
    self._cursorObservers.append(observer)

  def unsubscribe_cursorObserver(self, observer: CursorObserver):
    self._cursorObservers.remove(observer)

  def notify_cursorObservers(self):
    for observer in self._cursorObservers:
      observer.updateCursorLocation(self.cursorLocation)
  
  def subscribe_textObserver(self, observer: TextObserver):
    self._textObservers.append(observer)

  def unsubscribe_textObserver(self, observer: TextObserver):
    self._textObservers.remove(observer)

  def notify_textObservers(self):
    for observer in self._textObservers:
      observer.updateText()

  def moveCursorLeft(self):
    success = True
    if self.cursorLocation.column == 0:
      if self.cursorLocation.row == 0:
        success = False
      else:
        self.cursorLocation.row -= 1
        self.cursorLocation.column = len(self.lines[self.cursorLocation.row])
    else:
      self.cursorLocation.column -= 1
    if success:
      self.notify_cursorObservers()
    return success

  def moveCursorRight(self):
    success = True
    if self.cursorLocation.column == len(self.lines[self.cursorLocation.row]):
      if self.cursorLocation.row == len(self.lines) - 1:
        success = False
      else:
        self.cursorLocation.row += 1
        self.cursorLocation.column = 0
    else:
      self.cursorLocation.column += 1
    if success:
      self.notify_cursorObservers()
    return success
  
  def moveCursorUp(self):
    success = True
    if self.cursorLocation.row == 0:
      success = False
    else:
      self.cursorLocation.row -= 1
      self.cursorLocation.column = min(self.cursorLocation.column, len(self.lines[self.cursorLocation.row]))  
    if success:
      self.notify_cursorObservers()
    return success
  
  def moveCursorDown(self):
    success = True
    if self.cursorLocation.row == len(self.lines) - 1:
      success = False
    else:
      self.cursorLocation.row += 1
      self.cursorLocation.column = min(self.cursorLocation.column, len(self.lines[self.cursorLocation.row]))  
    if success:
      self.notify_cursorObservers()
    return success
  

  def deleteBefore(self):
    if self.cursorLocation.column == 0:
      if self.cursorLocation.row == 0:
        return False
      else:
        self.lines[self.cursorLocation.row - 1] += self.lines[self.cursorLocation.row]
        self.cursorLocation.column = len(self.lines[self.cursorLocation.row])
        self.lines.pop(self.cursorLocation.row)
        self.cursorLocation.row -= 1
    else:
      self.lines[self.cursorLocation.row] = self.lines[self.cursorLocation.row][:self.cursorLocation.column - 1] + self.lines[self.cursorLocation.row][self.cursorLocation.column:]
      self.cursorLocation.column -= 1
    self.notify_textObservers()
    self.notify_cursorObservers()
    return True
  
  def deleteAfter(self):
    if self.cursorLocation.column == len(self.lines[self.cursorLocation.row]):
      if self.cursorLocation.row == len(self.lines) - 1:
        return False
      else:
        self.lines[self.cursorLocation.row] += self.lines[self.cursorLocation.row + 1]
        self.lines.pop(self.cursorLocation.row + 1)
    else:
      self.lines[self.cursorLocation.row] = self.lines[self.cursorLocation.row][:self.cursorLocation.column] + self.lines[self.cursorLocation.row][self.cursorLocation.column + 1:]
    self.notify_textObservers()
    return True

  def deleteRange(self, r: LocationRange):
    if self.cursorLocation == Location(0, 0):
      return

    start = r.LocationRange.locationStart
    end = self.cursorLocation
    deleted_text = self.get_text_range(start, end)

    action = DeleteAction(self, start, end, deleted_text)
    self.undoManager.push(action)
    action.execute_do()

  def delete_range(self, r: LocationRange):
    start = r.locationStart
    end = r.locationEnd
    if (start.row > end.row) or (start.row == end.row and start.column > end.column):
      start, end = end, start

    if start.row == end.row:
        self.lines[start.row] = (
          self.lines[start.row][:start.column] +
          self.lines[end.row][end.column:]
        )
    else:
      first = self.lines[start.row][:start.column]
      last = self.lines[end.row][end.column:]
      self.lines[start.row] = first + last
      del self.lines[start.row + 1:end.row + 1]

    self.cursorLocation = Location(start.row, start.column)

    self.notify_textObservers()
    self.notify_cursorObservers()
  
  def getSelectionRange(self) -> LocationRange:
    return self._selectionRange
  
  def setSelectionRange(self, r: LocationRange):
    self._selectionRange = r
    self.notify_textObservers() # new

  def insert(self, txt: str):
    loc_copy = self.cursorLocation.copy()
    action = InsertAction(self, loc_copy, txt)
    action.execute_do()
    self.undoManager.push(action)

  def insert_text(self, txt: str):
    loc = self.cursorLocation

    if txt == '\r' or txt == '\n': # check
      right_side = self.lines[loc.row][loc.column:]
      self.lines[loc.row] = self.lines[loc.row][:loc.column]
      self.lines.insert(loc.row + 1, right_side)
      self.cursorLocation = Location(loc.row + 1, 0)
    else:
      new_lines = txt.splitlines() # we'll see
      before = self.lines[loc.row][:loc.column]
      after = self.lines[loc.row][loc.column:]
      self.lines[loc.row] = before + new_lines[0]

      current_row = loc.row
      current_col = len(before + new_lines[0])

      for i in range(1, len(new_lines) - 1):
        current_row += 1
        self.lines.insert(current_row, new_lines[i])

      if len(new_lines) > 1:
        current_row += 1
        self.lines.insert(current_row, new_lines[-1] + after)
        current_col = len(new_lines[-1])
      else:
        self.lines[current_row] += after

      self.cursorLocation = Location(current_row, current_col)

    self.notify_cursorObservers()
    self.notify_textObservers()

  def getSelectedText(self, r) -> str:
    if not r:
      return ''
    
    start = r.locationStart
    end = r.locationEnd

    if (start.row > end.row) or (start.row == end.row and start.column > end.column):
      start, end = end, start

    if start.row == end.row:
      return self.lines[start.row][start.column:end.column]
    else:
      selected_lines = []
      selected_lines.append(self.lines[start.row][start.column:])
      for row in range(start.row + 1, end.row):
        selected_lines.append(self.lines[row])
      selected_lines.append(self.lines[end.row][:end.column])
      return '\n'.join(selected_lines)


    
  
