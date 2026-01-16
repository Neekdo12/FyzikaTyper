import json
from tkinter import filedialog
import tkinter
from typing import Callable
import customtkinter as ctk

class SettingsHelper():
    def __init__(self) -> None:
        self.file_types: dict[str, tuple[tuple[str, str], tuple[str, str]]] = {
            "docx": (('word documents', '*.docx'), ('All files', '*.*')),
            "json": (('json data', '*.json'), ('All files', '*.*'))
        }
    
    def chose_file(self, filetype: tuple[tuple[str, str], tuple[str, str]]) -> Callable[[], str]:
        def run() -> str:
            return filedialog.askopenfilename(filetypes=filetype, initialdir="./saves")

        return run
    
    def create_save(self) -> str:
        return filedialog.asksaveasfilename(filetypes=self.file_types["json"])

class Settings(SettingsHelper):
    def __init__(self, path: str = "saves/settings.json") -> None:
        super().__init__()
        self.path: str = path
        self.data: dict[str, str | float | int] = {}

        self.load()
    
    def __call__(self, param: str, ask: Callable | str, rr: bool = False) -> str | float | int:
        if param in self.data and not rr:
            self.save()
            return self.data[param]
        
        self.data[param] = ask() if not (isinstance(ask, str)) else ask
        self.save()
        return self.data[param]
    
    def load(self) -> None:
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
    def save(self) -> None:
        with open(self.path, "w") as file:
            json.dump(self.data, file, indent=4)

class SettingsSetterPart(ctk.CTkFrame):
    def __init__(self, master, settings: Settings) -> None:
        super().__init__(master, height=100)

class SettingsSetterPartEntry(SettingsSetterPart):
    def __init__(self, master, settings, text, settings_name, default) -> None:
        super().__init__(master, settings)

        self.info_label: ctk.CTkLabel = ctk.CTkLabel(self, text=text)
        self.tk_var: ctk.StringVar = ctk.StringVar(self, value=settings(settings_name, lambda: default))
        self.entry: ctk.CTkEntry = ctk.CTkEntry(self, textvariable=self.tk_var)

        self.info_label.pack(side = "left", padx = 3, pady = 3)
        self.entry.pack(side = "right", padx = 3, pady = 3)

class SettingsSetterPartBox(SettingsSetterPart):
    def __init__(self, master, settings: Settings, text: str, settings_name: str, default: str, options: list[str]) -> None:
        super().__init__(master, settings)

        self.info_label: ctk.CTkLabel = ctk.CTkLabel(self, text=text)
        self.tk_var: ctk.StringVar = ctk.StringVar(self, value=str(settings(settings_name, lambda: default)))
        self.box: ctk.CTkOptionMenu = ctk.CTkOptionMenu(self, values=options, variable=self.tk_var)

        self.info_label.pack(side = "left", padx = 3, pady = 3)
        self.box.pack(side = "right", padx = 3, pady = 3)
    
class SettingsSetter(ctk.CTkToplevel):
    def __init__(self, settings: Settings, master) -> None:
        super().__init__()

        self.geometry("500x500")
        self.settings: Settings = settings

        self.prefix: SettingsSetterPartEntry = SettingsSetterPartEntry(self, settings, "Prefix for importing into word", "prefix", "zt")
        self.index_mode: SettingsSetterPartBox = SettingsSetterPartBox(self, settings, "What should happen when pressing key for indexing", "index_mode", "toggle", ["toggle", "hold"])
        self.smart_index: SettingsSetterPartBox = SettingsSetterPartBox(self, settings, "What should happen when pressing key for indexing", "smart_index", "off", ["off", "on"])
        self.export_style: SettingsSetterPartBox = SettingsSetterPartBox(self, settings, "What style should be used for exporting into word document", "export_style", "internal", ["none", "internal", "custom"])
        self.custom_style: SettingsSetterPartEntry = SettingsSetterPartEntry(self, settings, "Name of the custom style", "custom_style", "zt-style")

        self.buttons: ctk.CTkFrame = ctk.CTkFrame(self)
        self.buttons_ok: ctk.CTkButton = ctk.CTkButton(self.buttons, text="ok", command=self.ok)
        self.buttons_close: ctk.CTkButton = ctk.CTkButton(self.buttons, text="close")

        self.prefix.place(x = 0, y = 0, relwidth = 1, relheight = 1 / 13)
        self.index_mode.place(x = 0, rely = 1 / 13, relwidth = 1, relheight = 1 / 13)
        self.smart_index.place(x = 0, rely = 2 / 13, relwidth = 1, relheight = 1 / 13)
        self.export_style.place(x = 0, rely = 3/ 13, relwidth = 1, relheight = 1 / 13)
        self.custom_style.place(x = 0, rely = 4 / 13, relwidth = 1, relheight = 1 / 13)

        self.buttons_ok.pack(side = "right", expand = True, fill = "both", padx = 3, pady = 3)
        self.buttons_close.pack(side = "left", expand = True, fill = "both", padx = 3, pady = 3)
        self.buttons.place(relx = 0, rely = 1 - 1/13, relwidth = 1, relheight = 1/13)

        self.grab_set()
        self.focus()
        master.wait_window(self)
    
    def ok(self) -> None:
        if self.prefix.tk_var == "":
            raise Exception("Empty prefix entry - invalid value")

        self.settings.data["prefix"] = self.prefix.tk_var.get()
        self.settings.data["index_mode"] = self.index_mode.tk_var.get()
        self.settings.data["smart_index"] = self.smart_index.tk_var.get()
        self.settings.data["export_style"] = self.export_style.tk_var.get()
        self.settings.data["custom_style"] = self.custom_style.tk_var.get()

        self.settings.save()
        self.grab_release()
        self.destroy()