import tkinter as tk
import tkinter.font as tk_font
import clipboard as cb
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import messagebox


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Text Editor - Untitled')

        self.geometry('400x500+200+100')
        self.minsize(300, 450)

        self.filepath = None

        # Text Editor
        self.txt_editor = tk.Text(self, undo=True, autoseparators=True, maxundo=-1)
        self.font_family = 'Times New Roman'
        self.font_size = 12
        self.txt_editor.configure(font=tk_font.Font(family=self.font_family, size=self.font_size))
        self.txt_editor.pack(fill=tk.BOTH, expand=True)

        # Menu Bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        # File Menu
        self.file_menu = tk.Menu(self.menubar, tearoff=0)
        self.file_menu.add_command(label='New', command=lambda: App().mainloop())
        self.file_menu.add_command(label='Open', command=self.open_file)
        self.file_menu.add_command(label='Save', command=self.save_file)
        self.file_menu.add_command(label='Save As...', command=self.save_as)
        self.file_menu.add_separator()
        self.file_menu.add_command(label='Exit', command=self.on_closing)
        self.menubar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menubar, tearoff=0)
        self.edit_menu.add_command(label='Undo', command=self.txt_editor.edit_undo)
        self.edit_menu.add_command(label='Redo', command=self.txt_editor.edit_redo)
        self.edit_menu.add_separator()
        self.edit_menu.add_command(label='Cut', command=self.cut)
        self.edit_menu.add_command(label='Copy', command=self.copy)
        self.edit_menu.add_command(label='Paste', command=self.paste)
        self.menubar.add_cascade(label="Edit", menu=self.edit_menu)

        # View Menu
        self.view_menu = tk.Menu(self.menubar, tearoff=0)
        self.view_menu.add_command(label='Zoom In', command=self.zoom_in)
        self.view_menu.add_command(label='Zoom Out', command=self.zoom_out)
        self.menubar.add_cascade(label="View", menu=self.view_menu)

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def open_file(self):
        filepath = askopenfilename(
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')]
        )

        if not filepath:
            return

        self.txt_editor.delete(1.0, tk.END)
        with open(filepath, 'r') as input_file:
            content = input_file.read()
            self.txt_editor.insert(tk.END, content)

        self.filepath = filepath
        self.title(filepath)
        self.txt_editor.edit_modified(False)

    def save_file(self):
        if self.filepath:
            with open(self.filepath, 'w') as output_file:
                text = self.txt_editor.get(1.0, tk.END)
                output_file.write(text)
            self.txt_editor.edit_modified(False)
        else:
            self.save_as()

    def save_as(self):
        filepath = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
        )

        if not filepath:
            return

        with open(filepath, 'w') as output_file:
            text = self.txt_editor.get(1.0, tk.END)
            output_file.write(text)

        self.filepath = filepath
        self.title(f'Text Editor - {filepath}')
        self.txt_editor.edit_modified(False)

    def cut(self):
        content = self.txt_editor.selection_get()

        try:
            index_start = self.txt_editor.index("sel.first")
            index_end = self.txt_editor.index("sel.last")
        except tk.TclError:
            index_start = index_end = self.txt_editor.index(tk.INSERT)

        self.txt_editor.delete(index_start, index_end)
        cb.copy(content)

    def copy(self):
        content = self.txt_editor.selection_get()
        cb.copy(content)

    def paste(self):
        content = cb.paste()
        position = self.txt_editor.index(tk.INSERT)
        self.txt_editor.insert(position, content)

    def zoom_in(self):
        if self.font_size < 36:
            self.font_size += 1
            self.txt_editor.configure(font=tk_font.Font(family=self.font_family, size=self.font_size))

    def zoom_out(self):
        if self.font_size > 8:
            self.font_size -= 1
            self.txt_editor.configure(font=tk_font.Font(family=self.font_family, size=self.font_size))

    def on_closing(self):
        print(self.txt_editor.edit_modified())
        if self.filepath is not None and not self.txt_editor.edit_modified():
            self.destroy()
        elif messagebox.askokcancel(
            "Quit",
            "You have unsaved changes.\nDo you still want to quit?"
        ):
            self.destroy()


if __name__ == '__main__':
    app = App()
    app.mainloop()
