from asyncio.base_tasks import _task_print_stack
from typing import Callable
import customtkinter as ctk
import keyboard
from string import ascii_lowercase
import json

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
        self.create_window("My first window", None)

        self.create_hotkeys()

        self.windows_bar_frame.set_window(0)("")
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
            self.hotkeys.append(keyboard.add_hotkey(prefix + "shift+1", callback=self.type_key("+", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "altgr+-", callback=self.type_key("*", i)))

            self.hotkeys.append(keyboard.add_hotkey(prefix + "é", callback=self.type_key("0", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "1", callback=self.type_key("1", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "ě", callback=self.type_key("2", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "š", callback=self.type_key("3", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "č", callback=self.type_key("4", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "ř", callback=self.type_key("5", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "ž", callback=self.type_key("6", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "ý", callback=self.type_key("7", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "á", callback=self.type_key("8", i)))
            self.hotkeys.append(keyboard.add_hotkey(prefix + "í", callback=self.type_key("9", i)))
        
        # self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+s", callback=self.save))
        # self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+l", callback=self.load))
        self.hotkeys.append(keyboard.add_hotkey("ctrl+alt+n", callback=self.new_window))
    
    def clear_hotkeys(self) -> None:
        for i in self.hotkeys:
            keyboard.remove_hotkey(i)
    
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

if __name__ == "__main__":
    App()