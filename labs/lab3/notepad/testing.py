from texteditor import TextEditor; from texteditormodel import TextEditorModel
import tkinter as tk

text = """This is short
This is very very long
This is short"""
tem = TextEditorModel(text)
root = tk.Tk()
root.title('Fartpad')
te = TextEditor(root, tem, width=300, height=300)
te.pack(fill=tk.BOTH, expand=True)
root.mainloop()
