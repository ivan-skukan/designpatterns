from plugins.plugin import Plugin

class CapitalLetterPlugin(Plugin):
  def getName(self): return "Capitalize"

  def getDescription(self): return "Capitalizes first letter of each word"

  def execute(self, model, undoManager, clipboardStack):
    new_lines = []
    for line in model.lines:
      new_line = " ".join(word.capitalize() for word in line.split())
      new_lines.append(new_line)
    
    model.lines = new_lines
    model.notify_textObservers()