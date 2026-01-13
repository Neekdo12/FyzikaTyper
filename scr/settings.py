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

class SettingsSetterPartEntry(SettingsSetterPart):
    def __init__(self, master, settings, text, settings_name, default):
        super().__init__(master, settings)

        self.info_label = ctk.CTkLabel(self, text=text)
        self.tk_var = ctk.StringVar(self, value=settings(settings_name, lambda: default))
        self.entry = ctk.CTkEntry(self, textvariable=self.tk_var)

        self.info_label.pack(side = "left", padx = 3, pady = 3)
        self.entry.pack(side = "right", padx = 3, pady = 3)
    
class SettingsSetter(ctk.CTkToplevel):
    def __init__(self, settings: Settings, master):
        super().__init__()

        self.geometry("500x500")
        self.settings = settings

        self.prefix = SettingsSetterPartEntry(self, settings, "Prefix for importing into word", "prefix", "zt")

        self.buttons = ctk.CTkFrame(self)
        self.buttons_ok = ctk.CTkButton(self.buttons, text="ok", command=self.ok)
        self.buttons_close = ctk.CTkButton(self.buttons, text="close")

        self.prefix.place(x = 0, y = 0, relwidth = 1, relheight = 1 / 13)

        self.buttons_ok.pack(side = "right", expand = True, fill = "both", padx = 3, pady = 3)
        self.buttons_close.pack(side = "left", expand = True, fill = "both", padx = 3, pady = 3)
        self.buttons.place(relx = 0, rely = 1 - 1/13, relwidth = 1, relheight = 1/13)

        self.grab_set()
        self.focus()
        master.wait_window(self)
    
    def ok(self):
        if self.prefix.tk_var == "":
            raise Exception("Empty prefix entry - invalid value")
        
        self.settings.data["prefix"] = self.prefix.tk_var.get()

        self.settings.save()
        self.grab_release()
        self.destroy()