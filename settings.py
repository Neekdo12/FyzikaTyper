import json
from tkinter import filedialog

class SettingsHelper():
    def __init__(self):
        self.file_types = {
            "docx": (('word documents', '*.docx'), ('All files', '*.*')),
            "json": (('json data', '*.json'), ('All files', '*.*'))
        }
    
    def chose_file(self, filetype):
        def run():
            return filedialog.askopenfilename(filetypes=filetype, initialdir="./")

        return run

class Settings(SettingsHelper):
    def __init__(self, path: str = "settings.json"):
        super().__init__()
        self.path = path
        self.data = {}

        self.load()
    
    def __call__(self, param: str, ask):
        if param in self.data:
            return self.data[param]
        
        self.data[param] = ask()
        return self.data[param]
    
    def load(self):
        with open(self.path, "r") as file:
            self.data = json.load(file)
    
