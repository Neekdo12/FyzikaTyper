import customtkinter as ctk
import keyboard

class App(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.geometry("700x300")
        self.title("Typer")
        self.config(bg="black")

        self.cursor = ctk.CTkFrame(self, fg_color="white", width=2)
        self.line = 2

        self.lines = [Line(self, text="A * B = C"), Line(self, text="v / t = a"), Line(self, text="s0 + v0 * t + 1/2 * a * t ** 2 = s")]
        for i, v in enumerate(self.lines):
            v.place(x = 0, rely = 0.1 * i, relwidth = 1, relheight = 0.1)
        
        self.cursor.lift()
        self.cursor.place(x = self.lines[0].dict_counter, rely = 0.1 * self.line, relheight = 0.1)
        keyboard.add_hotkey("right", callback=self.on_direction_click_side(1))
        keyboard.add_hotkey("left", callback=self.on_direction_click_side(-1))
        keyboard.add_hotkey("up", callback=self.on_direction_click_height(-1))
        keyboard.add_hotkey("down", callback=self.on_direction_click_height(1))

        self.mainloop()
    
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

            self.lines[self.line].place_forget()
            self.lines[self.line].place(x = 0, rely = 0.1 * self.line, relwidth = 1, relheight = 0.1)
            self.lines[self.line].rerender()
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
    def __init__(self, master, text = "Noneni"):
        super().__init__(master=master, fg_color="black", corner_radius=0)

        self.normal_font = ctk.CTkFont(family="Consolas", size=30)
        self.normal_leter_size = self.normal_font.measure("A") + 0.5
        self.small_font = ctk.CTkFont(family="Consolas", size=17)
        self.small_letter_site = self.small_font.measure("B")

        self.labels: list[ctk.CTkLabel] = []

        self.letter_list: list[Letter] = [Letter(i) for i in text]
        self.letter_list.append(Letter("g", orient="d"))
        self.letter_list.append(Letter("g"))
        self.letter_list.append(Letter("2", orient="u"))
        self.letter_list.append(Letter(" "))
        self.letter_list.append(Letter("t"))
        self.letter_list.append(Letter("A", orient="d"))
        self.letter_list.append(Letter("2", orient="d"))
        self.letter_list.append(Letter("2", orient="u"))
        self.letter_tuple = []
        self.letter_pointer: int = 10

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

class Letter():
    def __init__(self, letter: str, orient: str | None = None) -> None:
        self.letter = letter
        self.orient = orient if orient is not None else "n"
    
    def get_tuple(self):
        return (self.letter, self.orient)

if __name__ == "__main__":
    App()