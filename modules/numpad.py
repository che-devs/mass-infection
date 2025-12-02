import customtkinter as ctk


class NumPad:
    def __init__(self):

        ctk.set_appearance_mode("Dark")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
    
        self.root = ctk.CTk()
        self.root.title("NumPad")
        self.root.geometry("640x480")
        self.root.after(1000, lambda: self.root.wm_attributes('-fullscreen', 'false'))
        self.root.bind('<Escape>', lambda e: self.root.quit())
        #self.root.attributes('-fullscreen', True)
        #self.root.attributes('-topmost', True)
        #self.root.overrideredirect(True)

        self.entry_var = ctk.StringVar()
        self.id = None
        self.enter_pushed = False

        self.barcode = ''
        self.barcode_entry = False

        self.create_widgets()

    def create_widgets(self):
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_rowconfigure(1, weight=1)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_rowconfigure(3, weight=1)
        self.root.grid_rowconfigure(4, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_columnconfigure(2, weight=1)

        self.entry_barcode = ctk.CTkEntry(self.root, width=200)
        self.entry_barcode.grid(row=5, column=0, padx=10, pady=10)
        self.entry_barcode.bind('<Return>', self.process_barcode)
        self.entry_barcode.after(10, self.entry_barcode.focus_set)

        self.entry = ctk.CTkEntry(
            self.root, textvariable=self.entry_var, font=("Arial", 48), justify="right"
        )
        self.entry.grid(row=0, column=0, columnspan=3, padx=20, pady=20, sticky="nsew")
        self.entry.configure(state='disabled')

        button_texts = [
            ("1", 1, 0),
            ("2", 1, 1),
            ("3", 1, 2),
            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("7", 3, 0),
            ("8", 3, 1),
            ("9", 3, 2),
            ("0", 4, 1),
        ]

        for text, row, col in button_texts:
            self.create_button(text, row, col)

        enter_button = ctk.CTkButton(
            self.root, text="Enter", command=self.on_enter, font=("Arial", 48)
        )
        enter_button.grid(row=4, column=2, padx=5, pady=5, sticky="nsew")

        exit_button = ctk.CTkButton(
            self.root, text="Delete", command=self.delete_entry, font=("Arial", 48)
        )
        exit_button.grid(row=4, column=0, padx=5, pady=5, sticky="nsew")

    def create_button(self, text, row, col):
        button = ctk.CTkButton(
            self.root,
            text=text,
            command=lambda: self.on_button_click(text),
            font=("Arial", 48),
        )
        button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew")
    
    def process_barcode(self, event=None):
        barcode = self.entry_barcode.get()
        """if len(barcode) == 12:
            barcode = barcode[:-1]
        barcode = barcode.rjust(12, '0')"""
        print('New Barcode:', barcode)
        self.barcode = barcode
        self.barcode_entry = True
        self.entry_barcode.delete(0, ctk.END)

    def on_button_click(self, char):
        current_text = self.entry_var.get()
        new_text = current_text + char
        self.entry_var.set(new_text)

    def on_enter(self):
        self.id = self.entry_var.get()
        #self.id = id.rjust(12, '0')
        self.entry_var.set("")
        print('Newe ID:', self.id)
        self.enter_pushed = True

    def delete_entry(self):
        self.entry_var.set("")

    def run(self):
        self.root.mainloop()

    def get_id(self):
        return self.id
    
    def new_id(self):
        if self.enter_pushed:
            self.enter_pushed = False
            return True
        else:
            return False
    
    def get_barcode(self):
        return self.barcode
    
    def new_barcode(self):
        if self.barcode_entry:
            self.barcode_entry = False
            return True
        else:
            return False


if __name__ == "__main__":
    numpad = NumPad()
    numpad.run()
