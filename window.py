import customtkinter as ctk
import json

from line import Line

class Window(ctk.CTkFrame):
    def __init__(self, master, content: list[list[tuple[str ,str]]] | None = None) -> None:
        super().__init__(master=master, fg_color="black")

        self.cursor = ctk.CTkFrame(self, fg_color="white", width=2)
        self.line = 0

        if content is None:
            self.lines = [Line(self, text="")]
            for i, v in enumerate(self.lines):
                v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        else:
            self.lines: list[Line] = []
            for i, v in enumerate(content):
                self.lines.append(Line(self, v))
                self.lines[-1].place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
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

    def save(self) -> list[list[tuple[str, str]]]:
        self.lines_tuple = []
        for i in self.lines:
            self.lines_tuple.append(i.letter_tuple)
        
        return self.lines_tuple
    
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