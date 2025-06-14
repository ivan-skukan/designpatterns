import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from texteditormodel import TextEditorModel
from cursorobserver import CursorObserver
from textobserver import TextObserver
from location import Location
from locationrange import LocationRange
from clipboardstack import ClipboardStack, ClipboardObserver
from plugins.plugin import Plugin
import importlib
import pkgutil
import inspect
import os

font_size = 15

class TextEditor(tk.Frame, CursorObserver, TextObserver, ClipboardObserver):
  def __init__(self, root, tem: TextEditorModel, **kwargs):
    super().__init__(root, **kwargs)
    self.root = root
    self._tem = tem
    self._clipboardStack = ClipboardStack()
    self._plugins = []

    self.menu = tk.Menu(root)
    self.root.config(menu=self.menu)
    self._setup_menu()

    self._canvas = tk.Canvas(self, bg='white')
    self._canvas.pack(fill=tk.BOTH, expand=True)

    self._status = tk.Label(self, text='', anchor='w')
    self._status.pack(fill=tk.X, side=tk.BOTTOM)

    self.font = tkfont.Font(family='Courier', size=font_size)
    self.char_width = self.font.measure('A')

    self._tem.subscribe_cursorObserver(self)
    self._tem.subscribe_textObserver(self)
    self._clipboardStack.add_observer(self)

    self._setup_binds()
    self.focus_set()
    self.updateDisplay()

  def _setup_menu(self):
  # File menu
    self.file_menu = tk.Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='File', menu=self.file_menu)

    self.file_menu.add_command(label='Open', command=self.open_file)
    self.open_index = self.file_menu.index('end')

    self.file_menu.add_command(label='Save', command=self.save_file)
    self.save_index = self.file_menu.index('end')

    self.file_menu.add_command(label='Exit', command=self.root.quit)
    self.exit_index = self.file_menu.index('end')

    # Edit menu
    self.edit_menu = tk.Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='Edit', menu=self.edit_menu)

    self.edit_menu.add_command(label='Undo', command=self._tem.undoManager.undo)
    self.undo_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Redo', command=self._tem.undoManager.redo)
    self.redo_index = self.edit_menu.index('end')

    self.edit_menu.add_separator()

    self.edit_menu.add_command(label='Cut', command=self.cut)
    self.cut_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Copy', command=self.copy)
    self.copy_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Paste', command=lambda: self.paste(False))
    self.paste_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Paste and Take', command=lambda: self.paste(True))
    self.paste_take_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Delete Section', command=self.delete_section)
    self.delete_section_index = self.edit_menu.index('end')

    self.edit_menu.add_command(label='Clear Document', command=lambda: self._tem.setText(''))
    self.clear_doc_index = self.edit_menu.index('end')

    # Move menu
    self.move_menu = tk.Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='Move', menu=self.move_menu)

    self.move_menu.add_command(label='Cursor to Start', command=lambda: self._tem.moveCursorTo(Location(0, 0)))
    self.cursor_start_index = self.move_menu.index('end')

    self.move_menu.add_command(label='Cursor to End', command=lambda: self._tem.moveCursorTo(Location(len(self._tem.lines) - 1, len(self._tem.lines[-1]))))
    self.cursor_end_index = self.move_menu.index('end')

    # Plugins menu
    self.plugins_menu = tk.Menu(self.menu, tearoff=0)
    self.load_plugins()

  def load_plugins(self):
    plugin_folder = 'plugins'
    for filename in os.listdir(plugin_folder):
      if filename.endswith('.py') and not filename.startswith('__'):
        filepath = os.path.join(plugin_folder, filename)
        module_name = f"plugins.{filename[:-3]}"

        spec = importlib.util.spec_from_file_location(module_name, filepath)
        if spec and spec.loader:
          module = importlib.util.module_from_spec(spec)
          spec.loader.exec_module(module)

          for _, obj in inspect.getmembers(module, inspect.isclass):
            if issubclass(obj, Plugin) and obj is not Plugin:
              instance = obj()
              self._plugins.append(instance)

              self.plugins_menu.add_command(
                label=instance.getName(),
                command=lambda p=instance: p.execute(self._tem, self._tem.undoManager, self._clipboardStack)
              )

    self.menu.add_cascade(label='Plugins', menu=self.plugins_menu)


  def _setup_binds(self):
    self.bind('<Key>', self.handle_key_press)
    self.bind('<Control-c>', lambda e: self.copy())
    self.bind('<Control-x>', lambda e: self.cut())
    self.bind('<Control-v>', lambda e: self.paste(False))
    self.bind('<Control-Shift-V>', lambda e: self.paste(True))
    self.bind('<Control-z>', lambda e: self._tem.undoManager.undo())
    self.bind('<Control-y>', lambda e: self._tem.undoManager.redo())

  def cut(self):
    selection = self._tem.getSelectionRange()
    if selection:
      text = self._tem.getSelectedText(selection)
      if text:
        self._clipboardStack.push(text)
        self._tem.deleteRange(selection)
        self._tem.setSelectionRange(None)
        self.updateMenu() # new

  def copy(self):
    selection = self._tem.getSelectionRange()
    if selection:
      text = self._tem.getSelectedText(selection)
      if text:
        self._clipboardStack.push(text)
        self.updateMenu() # new

  def paste(self, take=False):
    clip_text = self._clipboardStack.pop() if take else self._clipboardStack.peek()
    if clip_text:
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      self._tem.insert(clip_text)

  def delete_section(self):
    selection = self._tem.getSelectionRange()
    if selection:
      self._tem.deleteRange(selection)
      self._tem.setSelectionRange(None)


  def handle_key_press(self, event):
    shift = (event.state & 0x0001) != 0
    old_cursor = Location(self._tem.cursorLocation.row, self._tem.cursorLocation.column)
    moved = False

    if event.keysym in ('Left', 'Right', 'Up', 'Down'):
      moved = {
        'Left': self._tem.moveCursorLeft,
        'Right': self._tem.moveCursorRight,
        'Up': self._tem.moveCursorUp,
        'Down': self._tem.moveCursorDown,
      }[event.keysym]()

    elif event.keysym == 'Return' or (event.char and ord(event.char) >= 32):
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      self._tem.insert('\n' if event.keysym == 'Return' else event.char)

    elif event.keysym == 'BackSpace':
      if self._tem.getSelectionRange():
        self.delete_section()
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
      if shift:
        selection = self._tem.getSelectionRange() or LocationRange(old_cursor, new_cursor)
        self._tem.setSelectionRange(LocationRange(selection.locationStart, new_cursor))
      else:
        if self._tem.getSelectionRange():
          self._tem.setSelectionRange(None)

  def open_file(self):
    file_path = filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
      with open(file_path, 'r', encoding='utf-8') as file:
        self._tem.setText(file.read())
      self.updateDisplay()

  def save_file(self):
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
      with open(file_path, 'w', encoding='utf-8') as file:
        file.write(self._tem.getText())

  def updateDisplay(self):
    self.updateText()
    self.updateCursorLocation()

  def updateText(self):
    self.updateMenu()
    self.updateStatus() # does it make sense to update from update function?

    self._canvas.delete('text')
    self._canvas.delete('selection')

    selection = self._tem.getSelectionRange()
    for row, line in enumerate(self._tem.allLines()):
      if selection:
        start, end = selection.locationStart, selection.locationEnd
        if (start.row > end.row) or (start.row == end.row and start.column > end.column):
          start, end = end, start
        if start.row <= row <= end.row:
          x1 = (start.column if row == start.row else 0) * self.char_width
          x2 = (end.column if row == end.row else len(line)) * self.char_width
          y = row * (font_size + 5)
          self._canvas.create_rectangle(x1, y, x2, y + font_size + 2, fill='lightblue', tags='selection')

      self._canvas.create_text(0, row * (font_size + 5), text=line, font=self.font, anchor='nw', tags='text')

  def updateCursorLocation(self, loc: Location = None):
    self.updateMenu()
    self.updateStatus()

    self._canvas.delete('cursor')
    if loc is None:
      loc = self._tem.cursorLocation
    row, col = loc.row, loc.column
    x = col * self.char_width
    y = row * (font_size + 6)
    self._canvas.create_line(x, y, x, y + font_size, fill='black', width=3, tags='cursor')

  def updateMenu(self): # CHECK!!!!!!
    has_selection = self._tem.getSelectionRange() is not None
    has_undo = self._tem.undoManager.undoStack
    has_redo = self._tem.undoManager.redoStack
    clipboard_content = True if self._clipboardStack.peek() else False

    self.edit_menu.entryconfig(self.undo_index, state=tk.NORMAL if has_undo else tk.DISABLED)
    self.edit_menu.entryconfig(self.redo_index, state=tk.NORMAL if has_redo else tk.DISABLED)
    self.edit_menu.entryconfig(self.cut_index, state=tk.NORMAL if has_selection else tk.DISABLED)
    self.edit_menu.entryconfig(self.copy_index, state=tk.NORMAL if has_selection else tk.DISABLED)
    self.edit_menu.entryconfig(self.paste_index, state=tk.NORMAL if clipboard_content else tk.DISABLED)
    self.edit_menu.entryconfig(self.paste_take_index, state=tk.NORMAL if clipboard_content else tk.DISABLED)
    self.edit_menu.entryconfig(self.delete_section_index, state=tk.NORMAL if has_selection else tk.DISABLED)

  def updateStatus(self):
    cursor = self._tem.cursorLocation
    num_lines = len(self._tem.lines)
    self._status.config(text=f'Ln {cursor.row+1}, Col {cursor.column+1} | {num_lines} lines')

  def updateClipboard(self):
    pass
