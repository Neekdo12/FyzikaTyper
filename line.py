import customtkinter as ctk

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
            self.after(10, self.add_label(self.render_dict[i], i))

    def add_label(self, text, type):
        def run():
            if type[1] == "n":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.normal_font))
                self.labels[-1].pack(side = "left")
            elif type[1] == "d":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.small_font, anchor="sw"))
                self.labels[-1].pack(side = "left")
            elif type[1] == "u":
                self.labels.append(ctk.CTkLabel(self, text=text, font=self.small_font, anchor="nw"))
                self.labels[-1].pack(side = "left")
        
        return run
    
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