import tkinter as tk
# should probably rewrite this
class CustomComponent(tk.Canvas):
    def __init__(self, master=None, **kwargs):
        super().__init__(master, **kwargs)
        self.draw_elements()
        self.bind_all("<Return>", self.handle_enter)

    def draw_elements(self):
        width = int(self['width'])
        height = int(self['height'])

        self.create_line(0, height // 2, width, height // 2, fill="red", width=1)
        self.create_line(width // 2, 0, width // 2, height, fill="red", width=1)

        self.create_text(width // 2, height // 2 + 20, text="Ovo je prvi redak.", font=("Arial", 12))
        self.create_text(width // 2, height // 2 + 40, text="Ovo je drugi redak.", font=("Arial", 12))

    def handle_enter(self, event):
        self.master.destroy()

def main():
    root = tk.Tk()
    root.title("Custom Component")
    component = CustomComponent(root, width=300, height=200)
    component.pack()
    root.mainloop()

if __name__ == "__main__":
    main()
