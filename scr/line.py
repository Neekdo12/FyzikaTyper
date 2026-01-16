from typing import Callable
import customtkinter as ctk

class Line(ctk.CTkFrame):
    def __init__(self, master, text: str | list[tuple[str, str]] = "Noneni") -> None:
        super().__init__(master=master, fg_color="black", corner_radius=0)

        self.normal_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=30)
        self.normal_leter_size: float = self.normal_font.measure("A") + 0.5
        self.small_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=17)
        self.small_letter_site: float = self.small_font.measure("B") + 0.5

        self.labels: list[ctk.CTkLabel] = []
        self.unfinishd_labels: bool = False

        if isinstance(text, str):
            self.letter_list: list[Letter] = [Letter(i) for i in text]
        else:
            self.letter_list: list[Letter] = [Letter(i[0], orient=i[1]) for i in text]

        self.letter_tuple: list[tuple[str, str]] = []
        self.letter_pointer: int = 0

        self.render()

    def render(self) -> None:
        # Renders one line
        # Firstly is created list of tuples where one tuple corespond to one letter and it's index
        # Then the list is converted to dictionary with format xy: text where x is the number of normaly sized label, y is the index type, text is the text of the label
        # If there are more letters in row with the same index there are assigned to one customtkinter label
        self.render_dict: dict[str, str] = {}
        self.dict_pointer: int = -1
        self.dict_helper: str = ""
        self.count: bool = True
        self.dict_counter: float = 0
        self.letter_tuple: list[tuple[str, str]] = []

        # Creation of the tuple list
        for i in self.letter_list:
            self.letter_tuple.append(i.get_tuple())

        # Chceck for empty line
        if len(self.letter_tuple) == 0:
            self.dict_counter = 0
            return None
        
        # Creation of the rendering dict
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
        
        # Rendering loop, the rendering happens after 10 ms to prevent white flickering with customtkinter
        self.dict_pointer: int = 0
        self.dict_helper: str = list(self.render_dict.keys())[0][1]
        for i in self.render_dict:
            self.unfinishd_labels: bool = True
            self.after(10, self.add_label(self.render_dict[i], i))

    def add_label(self, text: str, type: str) -> Callable[[], None]:
        # The main rendering logick that adds labels
        def run() -> None:
            if type[1] == "n":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.normal_font))
                self.labels[-1].pack(side = "left")
            elif type[1] == "d":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.small_font, anchor="sw"))
                self.labels[-1].pack(side = "left")
            elif type[1] == "u":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.small_font, anchor="nw"))
                self.labels[-1].pack(side = "left")
            
            self.unfinishd_labels = False
        
        return run
    
    def rerender(self) -> None:
        # Delets everything and runs self.render()
        def run() -> None:
            for i in self.labels:
                i.pack_forget()
            self.labels.clear()

            self.render()

        if self.unfinishd_labels:
            self.after(10, run)
        else:
            run()
    
    def recount(self) -> None:
        # To know on wich position is cursor curently
        # Adds lenghts of each letter
        self.dict_counter: float = 0
        self.count: bool = True

        for num, i in enumerate(self.letter_tuple):
            if num == self.letter_pointer:
                self.count = False
                break

            if i[1] == "n":
                self.dict_counter += self.normal_leter_size if self.count else 0
            
            elif i[1] == "d":
                self.dict_counter += self.small_letter_site if self.count else 0
            
            elif i[1] == "u":
                self.dict_counter += self.small_letter_site if self.count else 0
    
    def delete(self) -> None:
        # Delets letter
        self.letter_list.pop(self.letter_pointer - 1)
        self.letter_pointer -= 1
    
    def add_key(self, key: str, type: str) -> None:
        # Add letter
        self.letter_list.insert(self.letter_pointer, Letter(key, orient=type))
        self.letter_pointer += 1

class Letter():
    # I do not know why this is not a simple tuple but it is how it is
    def __init__(self, letter: str, orient: str | None = None) -> None:
        self.letter: str = letter
        self.orient: str = orient if orient is not None else "n"
    
    def get_tuple(self) -> tuple[str, str]:
        return (self.letter, self.orient)