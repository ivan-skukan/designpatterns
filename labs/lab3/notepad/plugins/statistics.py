from plugins.plugin import Plugin
import tkinter as tk


class StatisticsPlugin(Plugin):
  def getName(self) -> str:
    return "Statistics Plugin"

  def getDescription(self) -> str:
    return "This plugin provides statistical analysis of data."

  def execute(self, *args):
    """assuming data is a list of strings"""
    if not args:
      return "No data provided for statistics."
    model = args[0]
    lines = model.lines

    num_lines = len(lines)
    num_words = sum(len(line.split()) for line in lines)
    num_chars = sum(len(line) for line in lines)
    
    data = {
      "Number of lines": num_lines,
      "Number of words": num_words,
      "Number of characters": num_chars
    }

    tk.messagebox.showinfo("Statistics", "\n".join(f"{key}: {value}" for key, value in data.items()))