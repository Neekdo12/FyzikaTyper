from typing import Callable
import customtkinter as ctk
import json

from line import Line

class Window(ctk.CTkFrame):
    def __init__(self, master, content: list[list[tuple[str ,str]]] | None = None) -> None:
        super().__init__(master=master, fg_color="black")

        self.cursor: ctk.CTkFrame = ctk.CTkFrame(self, fg_color="white", width=2)
        self.line: int = 0
        self.style_lines: list[ctk.CTkFrame] = []

        # Creates windows layout on load
        if content is None:
            self.lines = [Line(self, text="")]
            for i, v in enumerate(self.lines):
                v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        else:
            self.lines: list[Line] = []
            for i, v in enumerate(content):
                self.lines.append(Line(self, v))
                self.lines[-1].place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
        self.after(10, self.place_lines)
        
        self.cursor.lift()
        self.cursor.place(x = self.lines[0].dict_counter, rely = 0.1 * self.line, relheight = 0.1)
    
    
    def rerender(self, height_change: int = 0) -> None:
        # Places lines on screen after it delets them
        for i, v in enumerate(self.lines):
            v.place_forget()
            v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
        for i in self.style_lines:
            i.place_forget()
        self.style_lines.clear()        
        self.after(10, self.place_lines)

        self.on_direction_click_height(height_change)()
    
    def place_lines(self) -> None:
        # Only places lines on screen
        for i in range(1, 10):
            self.style_lines.append(ctk.CTkFrame(self, height=2))
            self.style_lines[-1].place(x = 0, rely = 0.1 * i, relwidth = 1)

    def save(self) -> list[list[tuple[str, str]]]:
        # Returns data for rebuilding window object
        self.lines_tuple: list[list[tuple[str, str]]] = []
        for i in self.lines:
            self.lines_tuple.append(i.letter_tuple)
        
        return self.lines_tuple
    
    def new_line(self) -> None:
        # Creates new line
        self.lines[self.line].letter_pointer = 0
        self.lines.insert(self.line + 1, Line(self, ""))
        self.cursor.lift()

        self.rerender(height_change=1)
    
    def rerender_line(self, line: int) -> None:
        self.lines[line].rerender()
    
    def type_key(self, key: str, type: str, ignor_keyboard: bool = False) -> Callable[[], None]:
        # Added new letter to place where is cursore
        def run() -> None:
            if not ignor_keyboard:
                if key == "3" and self.lines[self.line].letter_list[self.lines[self.line].letter_pointer - 1].get_tuple()[0] == "a":
                    self.lines[self.line].delete()

                if key == "5" and self.lines[self.line].letter_list[self.lines[self.line].letter_pointer - 1].get_tuple()[0] == "Y":
                    self.lines[self.line].delete()

            self.lines[self.line].add_key(key, type)
            self.rerender_line(self.line)
            self.on_direction_click_side(0)()

        return run
    
    def delete_char(self) -> None:
        # Delets letter
        self.lines[self.line].delete()
        self.rerender_line(self.line)
        self.on_direction_click_side(0)()
    
    def on_direction_click_side(self, val: int) -> Callable[[], None]:
        # Moves cursor horizobtaly
        def run() -> None:
            self.lines[self.line].letter_pointer += val

            # To wrap cursor on next line when you overflow the line on ringht
            if self.lines[self.line].letter_pointer > len(self.lines[self.line].letter_list):
                self.lines[self.line].letter_pointer = 0
                self.on_direction_click_height(1)()
                return None
            
            # To wrap cursor on previous line when you overflow the line on left
            if self.lines[self.line].letter_pointer == -1:
                self.lines[self.line].letter_pointer = len(self.lines[self.line - 1].letter_list)
                self.on_direction_click_height(-1)()
                return None
            
            # Rendres cursor
            self.lines[self.line].recount()
            self.cursor.place_forget()
            self.cursor.place(x = self.lines[self.line].dict_counter, rely = 0.1 * self.line, relheight = 0.1)

        return run
    
    def on_direction_click_height(self, val: int) -> Callable[[], None]:
        # Moves cursor verticaly
        def run() -> None:
            # Moves cursor to the start of the file when overflow hapens
            if self.line + 1 >= len(self.lines) and val > 0:
                self.line = 0

            # Moves cursor to the last line when overfllow hapens
            elif self.line - 1 == -1 and val < 0:
                self.line = len(self.lines) - 1
                self.lines[self.line].letter_pointer = self.lines[0].letter_pointer

                self.on_direction_click_side(0)()

                return None
            
            else:
                self.line += val

            # Renders cursor
            self.lines[self.line].letter_pointer = self.lines[self.line - val].letter_pointer
            self.on_direction_click_side(0)()
        
        return run