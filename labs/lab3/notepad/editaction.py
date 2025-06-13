from abc import ABC, abstractmethod
from locationrange import LocationRange
from location import Location

class EditAction(ABC):
  @abstractmethod
  def execute_do(self):
    pass
  @abstractmethod
  def execute_undo(self):
    pass


class InsertAction(EditAction):
  def __init__(self, model, location, text):
    self.model = model
    self.location = location
    self.text = text

  def execute_do(self):
    self.model.cursorLocation = self.location.copy()
    self.model.insert_text(self.text)

  def execute_undo(self):
    self.model.cursorLocation = self.location.copy()
    end_location = self._advance_location()
    self.model.delete_range(LocationRange(self.location, end_location))

  def _advance_location(self) -> Location:
    if self.text == '\r' or self.text == '\n':
      # better way to handle new lines?
      return Location(self.location.row + 1, 0)
    lines = self.text.splitlines()
    row = self.location.row
    col = self.location.column
    endl = row + len(lines) - 1
    endc = len(lines[-1]) if len(lines) > 1 else self.location.column + len(self.text)
    return Location(endl, endc)


class DeleteAction(EditAction):
  def __init__(self, model, location_range, deleted_text):
    self.model = model
    start = location_range.locationStart
    end = location_range.locationEnd

    if (start.row > end.row) or (start.row == end.row and start.column > end.column):
      start, end = end, start

    self.range = LocationRange(start.copy(), end.copy())
    self.deleted_text = deleted_text

  def execute_do(self):
    self.model.cursorLocation = self.range.locationStart.copy()
    self.model.delete_range(self.range)

  def execute_undo(self):
    self.model.cursorLocation = self.range.locationStart.copy()
    self.model.insert_text(self.deleted_text)
