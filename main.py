from sys import prefix
import customtkinter as ctk
import keyboard
from string import ascii_lowercase
import json

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("700x300")
        self.title("Typer")
        self.config(bg="black")

        self.cursor = ctk.CTkFrame(self, fg_color="white", width=2)
        self.line = 0

        self.lines = [Line(self, text="")]
        for i, v in enumerate(self.lines):
            v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
        self.cursor.lift()
        self.cursor.place(x = self.lines[0].dict_counter, rely = 0.1 * self.line, relheight = 0.1)
        keyboard.add_hotkey("right", callback=self.on_direction_click_side(1))
        keyboard.add_hotkey("left", callback=self.on_direction_click_side(-1))
        keyboard.add_hotkey("up", callback=self.on_direction_click_height(-1))
        keyboard.add_hotkey("down", callback=self.on_direction_click_height(1))
        
        keyboard.add_hotkey("backspace", callback=self.delete_char)
        keyboard.add_hotkey("enter", callback=self.new_line)

        for i in ascii_lowercase.removeprefix("") + "=-/.":
            keyboard.add_hotkey(i, callback=self.type_key(i, "n"))
            keyboard.add_hotkey(f"ctrl+{i}", callback=self.type_key(i, "d"))
            keyboard.add_hotkey(f"alt+{i}", callback=self.type_key(i, "u"))
        
        for i in ascii_lowercase.upper():
            keyboard.add_hotkey(f"shift+{i}", callback=self.type_key(i, "n"))
            keyboard.add_hotkey(f"ctrl+shift+{i}", callback=self.type_key(i, "d"))
            keyboard.add_hotkey(f"alt+shift+{i}", callback=self.type_key(i, "u"))

        for i in ("n", "d", "u"):
            if i == "n":
                prefix: str = ""
            elif i == "d":
                prefix = "ctrl+"
            else:
                prefix = "alt+"

            keyboard.add_hotkey(prefix + "space", callback=self.type_key(" ", i))
            keyboard.add_hotkey(prefix + "shift+1", callback=self.type_key("+", i))
            keyboard.add_hotkey(prefix + "altgr+-", callback=self.type_key("*", i))

            keyboard.add_hotkey(prefix + "é", callback=self.type_key("0", i))
            keyboard.add_hotkey(prefix + "1", callback=self.type_key("1", i))
            keyboard.add_hotkey(prefix + "ě", callback=self.type_key("2", i))
            keyboard.add_hotkey(prefix + "š", callback=self.type_key("3", i))
            keyboard.add_hotkey(prefix + "č", callback=self.type_key("4", i))
            keyboard.add_hotkey(prefix + "ř", callback=self.type_key("5", i))
            keyboard.add_hotkey(prefix + "ž", callback=self.type_key("6", i))
            keyboard.add_hotkey(prefix + "ý", callback=self.type_key("7", i))
            keyboard.add_hotkey(prefix + "á", callback=self.type_key("8", i))
            keyboard.add_hotkey(prefix + "í", callback=self.type_key("9", i))
        
        keyboard.add_hotkey("ctrl+alt+s", callback=self.save)
        keyboard.add_hotkey("ctrl+alt+l", callback=self.load)

        self.mainloop()
    
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
    
class Line(ctk.CTkFrame):
    def __init__(self, master, text: str | list[tuple[str, str]] = "Noneni"):
        super().__init__(master=master, fg_color="black", corner_radius=0)

        self.normal_font = ctk.CTkFont(family="Consolas", size=30)
        self.normal_leter_size = self.normal_font.measure("A") + 0.5
        self.small_font = ctk.CTkFont(family="Consolas", size=17)
        self.small_letter_site = self.small_font.measure("B") + 0.5

        self.labels: list[ctk.CTkLabel] = []

        if isinstance(text, str):
            self.letter_list: list[Letter] = [Letter(i) for i in text]
        else:
            self.letter_list: list[Letter] = [Letter(i[0], orient=i[1]) for i in text]

        self.letter_tuple = []
        self.letter_pointer: int = 0

        self.render()
        # self.test_text()

    def render(self) -> None:
        self.render_dict: dict[str, str] = {}
        self.dict_pointer = -1
        self.dict_helper: str = ""
        self.count = True
        self.dict_counter = 0
        self.letter_tuple = []

        for i in self.letter_list:
            self.letter_tuple.append(i.get_tuple())

        if len(self.letter_tuple) == 0:
            self.dict_counter = 0
            return None
        
        for num, i in enumerate(self.letter_tuple):
            if num == self.letter_pointer:
                self.count = False

            if i[1] == "n":
                self.dict_counter += self.normal_leter_size if self.count else 0
                if self.dict_helper == "n":
                    self.render_dict[f"{self.dict_pointer}n"] += i[0]
                else:
                    self.dict_pointer += 1
                    self.dict_helper = "n"
                    self.render_dict[f"{self.dict_pointer}n"] = i[0]
            
            if i[1] == "d":
                self.dict_counter += self.small_letter_site if self.count else 0
                if self.dict_helper == "d":
                    self.render_dict[f"{self.dict_pointer}d"] += i[0]
                else:
                    self.dict_helper = "d"
                    self.render_dict[f"{self.dict_pointer}d"] = i[0]
            
            if i[1] == "u":
                self.dict_counter += self.small_letter_site if self.count else 0
                if self.dict_helper == "u":
                    self.render_dict[f"{self.dict_pointer}u"] += i[0]
                else:
                    self.dict_helper = "u"
                    self.render_dict[f"{self.dict_pointer}u"] = i[0]
        
        self.dict_pointer = 0
        self.dict_helper: str = list(self.render_dict.keys())[0][1]
        for i in self.render_dict:
            if i[1] == "n":
                self.labels.append(ctk.CTkLabel(self, text=self.render_dict[i], font=self.normal_font))
                self.labels[-1].pack(side = "left")
            elif i[1] == "d":
                self.labels.append(ctk.CTkLabel(self, text=self.render_dict[i], font=self.small_font, anchor="sw"))
                self.labels[-1].pack(side = "left")
            elif i[1] == "u":
                self.labels.append(ctk.CTkLabel(self, text=self.render_dict[i], font=self.small_font, anchor="nw"))
                self.labels[-1].pack(side = "left")
    
    def rerender(self) -> None:
        for i in self.labels:
            i.pack_forget()
        self.labels.clear()
        
        self.render()
    
    def recount(self) -> None:
        self.dict_counter = 0
        self.count = True

        for num, i in enumerate(self.letter_tuple):
            if num == self.letter_pointer:
                self.count = False

            if i[1] == "n":
                self.dict_counter += self.normal_leter_size if self.count else 0
            
            elif i[1] == "d":
                self.dict_counter += self.small_letter_site if self.count else 0
            
            elif i[1] == "u":
                self.dict_counter += self.small_letter_site if self.count else 0
    
    def delete(self) -> None:
        self.letter_list.pop(self.letter_pointer - 1)
        self.letter_pointer -= 1
    
    def add_key(self, key: str, type: str) -> None:
        self.letter_list.insert(self.letter_pointer, Letter(key, orient=type))
        self.letter_pointer += 1

class Letter():
    def __init__(self, letter: str, orient: str | None = None) -> None:
        self.letter = letter
        self.orient = orient if orient is not None else "n"
    
    def get_tuple(self):
        return (self.letter, self.orient)

if __name__ == "__main__":
    App()