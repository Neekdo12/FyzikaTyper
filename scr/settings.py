import json
from tkinter import filedialog
import customtkinter as ctk

class SettingsHelper():
    def __init__(self):
        self.file_types = {
            "docx": (('word documents', '*.docx'), ('All files', '*.*')),
            "json": (('json data', '*.json'), ('All files', '*.*'))
        }
    
    def chose_file(self, filetype):
        def run():
            return filedialog.askopenfilename(filetypes=filetype, initialdir="./saves")

        return run
    
    def create_save(self):
        print("open")
        return filedialog.asksaveasfilename(filetypes=self.file_types["json"])

class Settings(SettingsHelper):
    def __init__(self, path: str = "saves/settings.json"):
        super().__init__()
        self.path = path
        self.data = {}

        self.load()
    
    def __call__(self, param: str, ask, rr: bool = False):
        if param in self.data and not rr:
            self.save()
            return self.data[param]
        
        self.data[param] = ask()
        self.save()
        return self.data[param]
    
    def load(self):
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
    def save(self):
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)

class SettingsSetterPart(ctk.CTkFrame):
    def __init__(self, master, settings: Settings):
        super().__init__(master, height=100)

class SettingsSetterPartPrefix(SettingsSetterPart):
    def __init__(self, master, settings):
        super().__init__(master, settings)

        self.info_label = ctk.CTkLabel(self, text="Word prefix")
        self.tk_var = ctk.StringVar(self, value=settings("prefix", lambda: "zt"))
        self.entry = ctk.CTkEntry(self, textvariable=self.tk_var)

        self.info_label.pack(side = "left")
        self.entry.pack(side = "right")
    
class SettingsSetter(ctk.CTkToplevel):
    def __init__(self, settings, master):
        super().__init__()

        self.geometry("300x500")

        self.prefix = SettingsSetterPartPrefix(self, settings)

        self.prefix.place(x = 0, y = 0, relwidth = 1, relheight = 1 / 13)

        self.grab_set()
        self.focus()
        master.wait_window(self)