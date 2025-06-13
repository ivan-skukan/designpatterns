import tkinter as tk
from tkinter import filedialog
import tkinter.font as tkfont
from texteditormodel import TextEditorModel
from cursorobserver import CursorObserver
from textobserver import TextObserver
from location import Location
from locationrange import LocationRange
from clipboardstack import ClipboardStack, ClipboardObserver

font_size = 15

class TextEditor(tk.Frame, CursorObserver, TextObserver, ClipboardObserver):
  def __init__(self, root, tem: TextEditorModel, **kwargs):
    super().__init__(root, **kwargs)
    self.root = root
    self._tem = tem
    self._clipboardStack = ClipboardStack()

    self.menu = tk.Menu(root)
    self.root.config(menu=self.menu)
    self._setup_menu()

    self._canvas = tk.Canvas(self, bg='white')
    self._canvas.pack(fill=tk.BOTH, expand=True)

    self.font = tkfont.Font(family='Courier', size=font_size)
    self.char_width = self.font.measure('A')

    self._tem.subscribe_cursorObserver(self)
    self._tem.subscribe_textObserver(self)
    self._clipboardStack.add_observer(self)

    self._setup_binds()
    self.focus_set()
    self.updateDisplay()

  def _setup_menu(self):
    file_menu = tk.Menu(self.menu, tearoff=0)
    file_menu.add_command(label='Open', command=self.open_file)
    file_menu.add_command(label='Save', command=self.save_file)
    file_menu.add_command(label='Exit', command=self.root.quit)
    self.menu.add_cascade(label='File', menu=file_menu)

    edit_menu = tk.Menu(self.menu, tearoff=0)
    edit_menu.add_command(label='Undo', command=self._tem.undoManager.undo)
    edit_menu.add_command(label='Redo', command=self._tem.undoManager.redo)
    edit_menu.add_separator()
    edit_menu.add_command(label='Cut', command=self.cut)
    edit_menu.add_command(label='Copy', command=self.copy)
    edit_menu.add_command(label='Paste', command=lambda: self.paste(False))
    edit_menu.add_command(label='Paste and Take', command=lambda: self.paste(True))
    edit_menu.add_command(label='Delete Section', command=self.delete_section)
    edit_menu.add_command(label='Clear Document', command=lambda: self._tem.setSelectionRange(None))
    self.menu.add_cascade(label='Edit', menu=edit_menu)

    move_menu = tk.Menu(self.menu, tearoff=0)
    move_menu.add_command(label='Cursor to Start', command=lambda: self._tem.moveCursorTo(Location(0, 0)))
    move_menu.add_command(label='Cursor to End', command=lambda: self._tem.moveCursorTo(Location(len(self._tem.lines) - 1, len(self._tem.lines[-1]))))
    self.menu.add_cascade(label='Move', menu=move_menu)

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

  def copy(self):
    selection = self._tem.getSelectionRange()
    if selection:
      text = self._tem.getSelectedText(selection)
      if text:
        self._clipboardStack.push(text)

  def paste(self, take=False):
    clip_text = self._clipboardStack.pop() if take else self._clipboardStack.peek()
    if clip_text:
      if self._tem.getSelectionRange():
        self._tem.deleteRange(self._tem.getSelectionRange())
        self._tem.setSelectionRange(None)
      self._tem.insert(clip_text)

  def delete_section(self):
    full_range = LocationRange(Location(0, 0), Location(len(self._tem.lines) - 1, len(self._tem.lines[-1])))
    self._tem.setSelectionRange(full_range)

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
    self._canvas.delete('cursor')
    if loc is None:
      loc = self._tem.cursorLocation
    row, col = loc.row, loc.column
    x = col * self.char_width
    y = row * (font_size + 6)
    self._canvas.create_line(x, y, x, y + font_size, fill='black', width=3, tags='cursor')

  def updateClipboard(self):
    pass
