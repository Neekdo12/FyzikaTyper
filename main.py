from typing import Callable
import customtkinter as ctk
import keyboard
from string import ascii_lowercase
import json
from pynput import keyboard

from window import Window
from window_helepr import WindowSwitcher, WindowLink

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("700x300")
        self.title("Typer")
        self.config(bg="black")

        self.windows_bar_frame: WindowSwitcher = WindowSwitcher(self)

        # self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self), title="My first window"))
        # self.create_window("My first window", None)
        self.load()

        self.create_hotkeys()

        self.windows_bar_frame.set_window(0)("")
        self.mainloop()
    
    def create_hotkeys(self) -> None:
        self.hotkeys: dict[str, Callable] = {}

        self.hotkeys["<right>"] = self.on_direction_click_side(1)
        self.hotkeys["<left>"] = self.on_direction_click_side(-1)
        self.hotkeys["<up>"] = self.on_direction_click_height(-1)
        self.hotkeys["<down>"] = self.on_direction_click_height(1)
        
        self.hotkeys["<backspace>"] = self.delete_char
        self.hotkeys["<enter>"] = self.new_line

        for i in ascii_lowercase.removeprefix("") + "=-/.":
            self.hotkeys[i] = self.type_key(i, "n")
            self.hotkeys[f"<ctrl>+{i}"] = self.type_key(i, "d")
            self.hotkeys[f"<alt>+{i}"] = self.type_key(i, "u")
        
        for i in ascii_lowercase.upper():
            self.hotkeys[f"<shift>+{i}"] = self.type_key(i, "n")
            self.hotkeys[f"<ctrl>+<shift>+{i}"] = self.type_key(i, "d")
            self.hotkeys[f"<alt>+<shift>+{i}"] = self.type_key(i, "u")

        for i in ("n", "d", "u"):
            if i == "n":
                prefix: str = ""
            elif i == "d":
                prefix = "<ctrl>+"
            else:
                prefix = "<alt>+"

            self.hotkeys[prefix + "<space>"] = self.type_key(" ", i)
            self.hotkeys[prefix + "<shift>+1"] = self.type_key("+", i)
            self.hotkeys[prefix + "<alt_gr>+-"] = self.type_key("*", i)

            self.hotkeys[prefix + "é"] = self.type_key("0", i)
            self.hotkeys[prefix + "1"] = self.type_key("1", i)
            self.hotkeys[prefix + "ě"] = self.type_key("2", i)
            self.hotkeys[prefix + "š"] = self.type_key("3", i)
            self.hotkeys[prefix + "č"] = self.type_key("4", i)
            self.hotkeys[prefix + "ř"] = self.type_key("5", i)
            self.hotkeys[prefix + "ž"] = self.type_key("6", i)
            self.hotkeys[prefix + "ý"] = self.type_key("7", i)
            self.hotkeys[prefix + "á"] = self.type_key("8", i)
            self.hotkeys[prefix + "í"] = self.type_key("9", i)
        
        self.hotkeys["<ctrl>+<alt>+s"] = self.save
        self.hotkeys["<ctrl>+<alt>+l"] = self.load
        self.hotkeys["<ctrl>+<alt>+n"] = self.new_window

        self.hotkeys_runner = keyboard.GlobalHotKeys(self.hotkeys)
        self.hotkeys_runner.start()
    
    def clear_hotkeys(self) -> None:
        self.hotkeys_runner.stop()
    
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
    
    def type_key(self, key, type):
        def run():
            self.windows_bar_frame.active_window().type_key(key, type)()
        
        return run

    def create_window(self, title, content):
        # test_line = [[("N", "n"), ("e", "d")], [("a", "n"), ("2", "u")]] # test for some small text sample
        self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self, content=content), title=title if title != "" else "Not defined"))
    
    def save(self):
        self.save_data = {}

        for i in self.windows_bar_frame.windows:
            self.save_data[i.title] = i.window.save()
        
        with open("save.json", "w") as file:
            json.dump(self.save_data, file)
    
    def load(self):
        with open("save.json", "r") as file:
            self.save_data = json.load(file)
        
        for i in self.save_data:
            self.create_window(i, self.save_data[i])


if __name__ == "__main__":
    App()