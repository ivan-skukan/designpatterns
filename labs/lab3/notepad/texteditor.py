import tkinter as tk
from texteditormodel import TextEditorModel
import tkinter.font as tkfont
from cursorobserver import CursorObserver
from textobserver import TextObserver
from location import Location
from locationrange import LocationRange
from clipboardstack import ClipboardStack, ClipboardObserver

font_size = 15

class TextEditor(tk.Frame, CursorObserver, TextObserver, ClipboardObserver):
  def __init__(self, root, tem: TextEditorModel=None, **kwargs):
    super().__init__(root, **kwargs)
    self.root = root

    self.menu = tk.Menu(root)
    self.root.config(menu=self.menu)
    
    self.menu_seutup()

    self._canvas = tk.Canvas(self, bg='white')
    self._canvas.pack(fill=tk.BOTH, expand=True)
    
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

  def menu_seutup(self):
    file_menu = tk.Menu(self.menu, tearoff=0) 
    self.menu.add_cascade(label='File', menu=file_menu)
    file_menu.add_command(label='Open', command=lambda: self.open_file())
    file_menu.add_command(label='Save', command=lambda: self.save_file())
    file_menu.add_command(label='Exit', command=self.root.quit)

    edit_menu = tk.Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='Edit', menu=edit_menu)
    edit_menu.add_command(label='Undo', command=lambda: self._tem.undoManager.undo())
    edit_menu.add_command(label='Redo', command=lambda: self._tem.undoManager.redo())
    edit_menu.add_separator()
    edit_menu.add_command(label='Cut', command=lambda: self.handle_key_press(tk.Event(keysym='x', state=0x0004)))  # Simulate CTRL+X
    edit_menu.add_command(label='Copy', command=lambda: self.handle_key_press(tk.Event(keysym='c', state=0x0004)))  # Simulate CTRL+C
    edit_menu.add_command(label='Paste', command=lambda: self.handle_key_press(tk.Event(keysym='v', state=0x0004)))  # Simulate CTRL+V
    edit_menu.add_command(label='Paste and Take', command=lambda: self.handle_key_press(tk.Event(keysym='v', state=0x0004 | 0x0001)))  # Simulate CTRL+SHIFT+V
    edit_menu.add_command(label='Delete Section', command=lambda: self._tem.setSelectionRange(LocationRange(Location(0, 0), Location(len(self._tem.lines) - 1, len(self._tem.lines[-1]))))) # fix
    edit_menu.add_command(label='Clear document', command=lambda: self._tem.setSelectionRange(None))  

    move_menu = tk.Menu(self.menu, tearoff=0)
    self.menu.add_cascade(label='Move', menu=move_menu)
    move_menu.add_command(label='Cursor to start', command=lambda: self._tem.moveCursorTo(Location(0, 0)))
    move_menu.add_command(label='Cursor to end', command=lambda: self._tem.moveCursorTo(Location(len(self._tem.lines) - 1, len(self._tem.lines[-1])))) 

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
    elif event.keysym == 'Return' or (event.char and event.keysym not in ('BackSpace', 'Delete') and ord(event.char) >= 32):
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
      return 'break'

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


  def open_file(self):
    file_path = tk.filedialog.askopenfilename(filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
      with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
      self._tem.setText(content) # or delete then insert?
      self.updateDisplay()

  def save_file(self):
    file_path = tk.filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
    if file_path:
      with open(file_path, 'w', encoding='utf-8') as file:
        file.write(self._tem.getText())

  def updateDisplay(self):
    self.updateText()
    self.updateCursorLocation() # is this good?
    
  def updateText(self):
    self._canvas.delete('text')
    self._canvas.delete('selection')

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

          self._canvas.create_rectangle(x1, y, x2, y + font_size + 2, fill='lightblue', tags='selection')

      self._canvas.create_text(0, row*(font_size+5), text=line, font=self.font, anchor='nw', tags='text')

  def updateCursorLocation(self, loc: Location = Location(0,0)):
    self._canvas.delete('cursor')
    row, column = loc.row, loc.column
    self._canvas.create_line(self.char_width*column,(row*(font_size+6)),self.char_width*column,(row*(font_size+6)+font_size), fill='black', width=3, tags='cursor')

  def updateClipboard(self):
    #useless
    pass
