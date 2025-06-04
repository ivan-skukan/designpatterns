from location import Location

class LocationRange:
  def __init__(self, locationStart: Location, locationEnd: Location):
    self.locationStart = locationStart
    self.locationEnd = locationEnd
  def copy(self):
    return LocationRange(self.locationStart.copy(), self.locationEnd.copy())

