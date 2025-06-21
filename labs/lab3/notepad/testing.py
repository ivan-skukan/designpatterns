from texteditor import TextEditor; from texteditormodel import TextEditorModel
import tkinter as tk

text = """"""
tem = TextEditorModel(text)
root = tk.Tk()
root.title('Txt editor')
te = TextEditor(root, tem, width=300, height=300)
te.pack(fill=tk.BOTH, expand=True)
root.mainloop()
