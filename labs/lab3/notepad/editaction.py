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
    lines = self.text.splitlines()
    row = self.location.row
    col = self.location.column
    endl = row + len(lines) - 1
    endc = len(lines[-1]) if len(lines) > 1 else self.location.column + len(self.text)
    return Location(endl, endc)


class DeleteAction(EditAction):
  def __init__(self, model, location_range, deleted_text):
    self.model = model
    self.range = location_range
    self.deleted_text = deleted_text

  def execute_do(self):
    self.model.cursorLocation = self.range.locationStart.copy()
    self.model.deleteRange(self.range)

  def execute_undo(self):
    self.model.cursorLocation = self.range.locationStart.copy()
    self.model.insert_text(self.deleted_text)
