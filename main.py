from asyncio.base_tasks import _task_print_stack
from typing import Callable
import customtkinter as ctk
import keyboard
from string import ascii_lowercase
import json

from line import Line

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("700x300")
        self.title("Typer")
        self.config(bg="black")

        self.windows_bar_frame = WindowSwitcher(self)

        self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self), title="My first window"))

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
        self.windows_bar_frame.add_window(WindowLink(self.windows_bar_frame, Window(self), title=title if title != "" else "Not defined"))
        
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

class WindowSwitcher(ctk.CTkScrollableFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master, orientation="horizontal", corner_radius=0)
        self._scrollbar.configure(height = 5)

        self.a_window: int = 0
        self.windows: list[WindowLink] = []

        self.place(x = 0, y = 0, relwidth = 1, relheight = 0.1)
    
    def add_window(self, window_link: WindowLink, main = False) -> None:
        self.windows.append(window_link)
        window_link.pack(side = "left", fill = "y", expand = True, padx = 3, pady = 1)

        if main:
            self.a_window = len(self.windows) - 1
            window_link.render()

    def set_window(self, window):
        def run(event): 
            self.windows[self.a_window].clear()
            self.a_window = window
            self.windows[self.a_window].render()
        
        return run

    def active_window(self) -> Window:
        return self.windows[self.a_window].window


class WindowLink(ctk.CTkFrame):
    id: int = 0

    def __init__(self, master, window: Window, title: str = "Undefined title") -> None:
        super().__init__(master=master, fg_color="#FF0000")
        self.window: Window = window

        self.label = ctk.CTkLabel(self, text=title)
        self.label.pack()

        self.label.bind("<Button-1>", master.set_window(WindowLink.id))
        self.bind("<Button-1>", master.set_window(WindowLink.id))
        WindowLink.id += 1
    
    def render(self) -> None:
        self.window.place(x = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
    
    def clear(self) -> None:
        self.window.place_forget()

class Window(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master)

        self.cursor = ctk.CTkFrame(self, fg_color="white", width=2)
        self.line = 0

        self.lines = [Line(self, text="")]
        for i, v in enumerate(self.lines):
            v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
        self.cursor.lift()
        self.cursor.place(x = self.lines[0].dict_counter, rely = 0.1 * self.line, relheight = 0.1)
    
    def rerender(self, height_change: int = 0) -> None:
        for i, v in enumerate(self.lines):
            v.place_forget()
            v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        self.on_direction_click_height(height_change)()
    
    def load(self) -> None:
        list(map(lambda line: line.place_forget(), self.lines))
        self.lines_tuple: list[list[tuple[str, str]]] = []
        self.line = 0

        with open("save.json", "r") as file:
            self.lines_tuple = json.load(file)["lines"]
        
        self.lines = []
        
        for i in self.lines_tuple:
            self.lines.append(Line(self, i))
        
        self.cursor.lift()
        self.rerender()

    def save(self) -> None:
        self.lines_tuple = []
        for i in self.lines:
            self.lines_tuple.append(i.letter_tuple)
        
        with open("save.json", "w") as file:
            json.dump({"lines": self.lines_tuple}, file, indent=4)
    
    def new_line(self) -> None:
        self.lines[self.line].letter_pointer = 0
        self.lines.insert(self.line + 1, Line(self, ""))
        self.cursor.lift()

        self.rerender(height_change=1)
    
    def rerender_line(self, line: int) -> None:
        self.lines[line].rerender()
    
    def type_key(self, key, type: str):
        def run():
            if key == "3" and self.lines[self.line].letter_list[self.lines[self.line].letter_pointer - 1].get_tuple()[0] == "a":
                self.lines[self.line].delete()

            elif key == "5" and self.lines[self.line].letter_list[self.lines[self.line].letter_pointer - 1].get_tuple()[0] == "y":
                self.lines[self.line].delete()

            self.lines[self.line].add_key(key, type)
            self.rerender_line(self.line)
            self.on_direction_click_side(0)()
        return run
    
    def delete_char(self) -> None:
        self.lines[self.line].delete()
        self.rerender_line(self.line)
        self.on_direction_click_side(0)()
    
    def on_direction_click_side(self, val: int):
        def run():
            self.lines[self.line].letter_pointer += val

            if self.lines[self.line].letter_pointer > len(self.lines[self.line].letter_list):
                self.lines[self.line].letter_pointer = 0
                self.on_direction_click_height(1)()
                return None
            
            if self.lines[self.line].letter_pointer == -1:
                self.lines[self.line].letter_pointer = len(self.lines[self.line - 1].letter_list)
                self.on_direction_click_height(-1)()
                return None

            # self.lines[self.line].place_forget()
            # self.lines[self.line].place(x = 0, rely = 0.1 * self.line, relwidth = 1, relheight = 0.1)
            self.lines[self.line].recount()
            self.cursor.place_forget()
            self.cursor.place(x = self.lines[self.line].dict_counter, rely = 0.1 * self.line, relheight = 0.1)

        return run
    
    def on_direction_click_height(self, val: int):
        def run():
            if self.line + 1 >= len(self.lines) and val > 0:
                self.line = 0

            elif self.line - 1 == -1 and val < 0:
                self.line = len(self.lines) - 1
                self.lines[self.line].letter_pointer = self.lines[0].letter_pointer

                self.on_direction_click_side(0)()

                return None
            
            else:
                self.line += val

            self.lines[self.line].letter_pointer = self.lines[self.line - val].letter_pointer
            self.on_direction_click_side(0)()
        
        return run

if __name__ == "__main__":
    App()