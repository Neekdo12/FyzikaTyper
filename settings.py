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
    
    def create_save(self):
        print("open")
        return filedialog.asksaveasfilename(filetypes=self.file_types["json"])

class Settings(SettingsHelper):
    def __init__(self, path: str = "settings.json"):
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
    
