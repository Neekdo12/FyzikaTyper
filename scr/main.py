from typing import Callable
import customtkinter as ctk
import keyboard
from string import ascii_lowercase
import json
from docx import Document

from settings import Settings, SettingsSetter
from window import Window
from window_helepr import WindowSwitcher, WindowLink
import docx_helper

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.settings = Settings()

        self.geometry("700x330")
        self.title("Typer")
        self.config(bg="black")

        self.down_index_smart = False
        self.down_index = False
        self.up_index = False
        self.up_index_smart = False

        self.windows_bar_frame: WindowSwitcher = WindowSwitcher(self)

        # self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self), title="My first window"))
        # self.create_window("My first window", None)
        self.load()

        self.create_hotkeys()

        self.windows_bar_frame.set_window(list(self.windows_bar_frame.windows)[0])("")
        self.mainloop()
    
    def create_hotkeys(self) -> None:
        self.hotkeys: list[Callable] = []

        self.hotkeys.append(keyboard.add_hotkey("right", callback=self.on_direction_click_side(1)))
        self.hotkeys.append(keyboard.add_hotkey("left", callback=self.on_direction_click_side(-1)))
        self.hotkeys.append(keyboard.add_hotkey("up", callback=self.on_direction_click_height(-1)))
        self.hotkeys.append(keyboard.add_hotkey("down", callback=self.on_direction_click_height(1)))
        
        self.hotkeys.append(keyboard.add_hotkey("backspace", callback=self.delete_char))
        self.hotkeys.append(keyboard.add_hotkey("enter", callback=self.new_line))

        for i in ascii_lowercase.removeprefix("") + "=-/.":
            self.hotkeys.append(keyboard.add_hotkey(i, callback=self.type_key(i, "n")))
            self.hotkeys.append(keyboard.add_hotkey(f"ctrl+{i}", callback=self.type_key(i, "d")))
            self.hotkeys.append(keyboard.add_hotkey(f"alt+{i}", callback=self.type_key(i, "u")))
        
        for i in ascii_lowercase.upper():
            self.hotkeys.append(keyboard.add_hotkey(f"shift+{i}", callback=self.type_key(i, "n")))
            self.hotkeys.append(keyboard.add_hotkey(f"ctrl+shift+{i}", callback=self.type_key(i, "d")))
            self.hotkeys.append(keyboard.add_hotkey(f"alt+shift+{i}", callback=self.type_key(i, "u")))

        for i in ("n", "d", "u"):
            if i == "n":
                prefix: str = ""
            elif i == "d":
                prefix = "ctrl+"
            else:
                prefix = "alt+"

            self.hotkeys.append(keyboard.add_hotkey(prefix + "space", callback=self.type_key(" ", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "1", callback=self.type_key("+", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "altgr+-", callback=self.type_key("*", i)))

            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+é", callback=self.type_key("0", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+1", callback=self.type_key("1", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+ě", callback=self.type_key("2", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+š", callback=self.type_key("3", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+č", callback=self.type_key("4", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+ř", callback=self.type_key("5", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+ž", callback=self.type_key("6", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+ý", callback=self.type_key("7", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+á", callback=self.type_key("8", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+í", callback=self.type_key("9", i)))
        
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+s", callback=self.save))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+c", callback=self.close_window))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+p", callback=self.change_settings))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+shift+s", callback=self.new_save))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+shift+n", callback=self.new_file))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+l", callback=self.load))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+shift+l", callback=self.force_load))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+n", callback=self.new_window))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+e", callback=self.export))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+right", callback=self.on_click_change_window(1)))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+left", callback=self.on_click_change_window(-1)))

        self.hotkeys.append(keyboard.add_hotkey("ctrl", callback=self.set_down_index))
        self.hotkeys.append(keyboard.add_hotkey("alt", callback=self.set_up_index))
    
    def clear_hotkeys(self) -> None:
        for i in self.hotkeys:
            keyboard.remove_hotkey(i)
    
    def export(self):
        self.save()
        docx_helper.export(self.save_data, Document(self.settings("docx", self.settings.chose_file(self.settings.file_types["docx"]))), self.settings)
    
    def on_click_change_window(self, val):
        def run():
            ac, len_windows = self.windows_bar_frame.a_window, len(self.windows_bar_frame.windows)

            """
            if ac + val >= len_windows:
                ac = 0
            elif ac + val == -1:
                ac = len_windows - 1
            else:
                ac += val
            """
            
            self.windows_bar_frame.set_window(ac)(None)

        return run
    
    def new_window(self) -> None:
        self.clear_hotkeys()

        title = str(ctk.CTkInputDialog(text="New window name:").get_input())
        self.create_window(title=title, content=None)
        
        self.after(10, lambda: self.create_hotkeys())
    
    def new_line(self):
        self.windows_bar_frame.active_window().new_line()
    
    def delete_char(self):
        self.windows_bar_frame.active_window().delete_char()
    
    def on_direction_click_side(self, val: int):
        def run():
            self.windows_bar_frame.active_window().on_direction_click_side(val)()
        
        return run

    def on_direction_click_height(self, val):
        def run():
            self.windows_bar_frame.active_window().on_direction_click_height(val)()
        
        return run
    
    def type_key(self, key, type2: str):
        def run():
            type = type2

            if self.settings("index_mode", "toggle") == "hold":
                if self.up_index:
                    type = "u"
                
                if self.down_index:
                    type = "d"
            
            if self.settings("smart_index", "off") == "on":
                if self.up_index_smart:
                    type = "u"
                
                if self.down_index_smart:
                    type = "d"
            
            if key in ascii_lowercase or key in ascii_lowercase.upper():
                self.down_index_smart = True
            
            elif key == " ":
                self.down_index_smart = False
                type = "n"
            
            self.windows_bar_frame.active_window().type_key(key, type)()
        
        return run

    def create_window(self, title, content):
        # test_line = [[("N", "n"), ("e", "d")], [("a", "n"), ("2", "u")]] # test for some small text sample
        self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self, content=content), title=title if title != "" else "Not defined"))
    
    def save(self):
        print("startings to save...")
        self.save_data = {}

        for i in self.windows_bar_frame.windows:
            print(f"saving: {i}")
            self.save_data[self.windows_bar_frame.windows[i].title] = self.windows_bar_frame.windows[i].window.save()
        
        with open(self.settings("save", self.settings.chose_file(self.settings.file_types["json"])), "w") as file:
            json.dump(self.save_data, file)
        
        print("saving done")
    
    def new_save(self):
        self.save()

        self.settings.data["save"] = self.settings.create_save().removesuffix(".json") + ".json"

        with open(self.settings.data["save"], "w") as file:
            json.dump(self.save_data, file, indent=4)
        print("Created new savefile")
    
    def new_file(self):
        self.save()
        self.reload()

        title = str(ctk.CTkInputDialog(text="New window name:").get_input())
        self.settings.data["save"] = self.settings.create_save().removesuffix(".json") + ".json"
        with open(self.settings.data["save"], "w") as file:
            json.dump({title: [[]]}, file, indent=4)
        
        self.load()
    
    def load(self):
        print("started loading...")
        with open(self.settings("save", self.settings.chose_file(self.settings.file_types["json"])), "r") as file:
            self.save_data = json.load(file)
        
        for i in self.save_data:
            print(f"loading: {i}")
            self.create_window(i, self.save_data[i])
        
        print("loading done")
    
    def force_load(self):
        print("started loading...")
        self.reload()

        with open(self.settings("save", self.settings.chose_file(self.settings.file_types["json"]), True), "r") as file:
            self.save_data = json.load(file)
        
        for i in self.save_data:
            print(f"loading: {i}")
            self.create_window(i, self.save_data[i])
        
        print("loading done")
    
    def reload(self):
        print("Saterted reloading")
        for i in self.windows_bar_frame.windows.copy():
            self.windows_bar_frame.remove_window(i)
        print("Reloading done")
    
    def change_settings(self):
        self.setter = SettingsSetter(self.settings, self)
    
    def close_window(self):
        self.windows_bar_frame.remove_window(self.windows_bar_frame.a_window)
    
    def set_up_index(self):
        self.up_index = not self.up_index
        self.down_index_smart = False
        self.up_index_smart = False
    
    def set_down_index(self):
        self.down_index = not self.down_index
        self.down_index_smart = False
        self.up_index_smart = False


if __name__ == "__main__":
    App()