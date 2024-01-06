import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename


class App(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title('Text Editor')

        self.geometry('400x500+200+100')
        self.minsize(300, 450)

        # Menu Bar
        self.menubar = tk.Menu(self)
        self.config(menu=self.menubar)

        self.file_menu = tk.Menu(self.menubar)

        self.file_menu.add_command(
            label='New',
            command=lambda: App().mainloop()
        )

        self.file_menu.add_command(
            label='Open',
            command=self.open_file
        )

        self.file_menu.add_command(
            label='Save As...',
            command=self.save_file
        )

        self.file_menu.add_separator()

        self.file_menu.add_command(
            label='Exit',
            command=self.destroy
        )

        self.menubar.add_cascade(
            label="File",
            menu=self.file_menu
        )

        # Text Editor
        self.txt_editor = tk.Text(self)
        self.txt_editor.pack(fill=tk.BOTH, expand=True)

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
        self.title(f'TextEditor - {filepath}')

    def save_file(self):
        filepath = asksaveasfilename(
            defaultextension='txt',
            filetypes=[('Text Files', '*.txt'), ('All Files', '*.*')],
        )

        if not filepath:
            return

        with open(filepath, 'w') as output_file:
            text = self.txt_editor.get(1.0, tk.END)
            output_file.write(text)
        self.title(f'Text Editor - {filepath}')


if __name__ == '__main__':
    app = App()
    app.mainloop()
