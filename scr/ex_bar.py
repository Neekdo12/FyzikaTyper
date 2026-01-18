import customtkinter as ctk
from typing import Callable
import keyboard

class exBar(ctk.CTkFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master, fg_color="#111010", border_color="#FFFFFF", border_width=3, width=350, height=150)

        self.master = master
        self.hotkeys = []
        self.exGroups = {
            f"kinematika": exGroup(self, "Kinematyka",),
            f"dynamika": exGroup(self, "Dynamika"),
            f"tuhe_teleso": exGroup(self, "Tuhe těleso"),
            f"prace": exGroup(self, "Mechanická práce"),
            f"astrofyzika": exGroup(self, "Astrofyzika"),
            }
        self.pointer = 0
        self.len: int = len(list(self.exGroups))
        self.state = "G"
        self.group_pointer = 0
        self.ret = ""

        self.exGroups[list(self.exGroups)[self.pointer]].activate()

    def show(self, letter: str, restor_func: Callable[[], None]) -> None:
        self.lift()
        self.place(relx = 0.25, y = 90, relwidth = 0.5, relheight = 150 / 330 + 0.01)

        self.hotkeys.append(keyboard.add_hotkey("esc", self.ok))

        self.hotkeys.append(keyboard.add_hotkey("up", self.down))
        self.hotkeys.append(keyboard.add_hotkey("down", self.up))

        self.hotkeys.append(keyboard.add_hotkey("tab", self.tab))
        self.hotkeys.append(keyboard.add_hotkey("enter", self.enter))
        self.restor_func: Callable[[], None] = restor_func

        self.grab_set()
        self.focus()

    def ok(self):
        for i in self.hotkeys:
            keyboard.remove_hotkey(i)
        self.hotkeys.clear()


        self.exGroups[list(self.exGroups)[self.pointer]].deactivate()
        self.exGroups[list(self.exGroups)[0]].activate()
        self.pointer = 0
        self.place_forget()
        self.restor_func()

        self.grab_release()
    
    def up(self) -> None:
        temp_pointer: int = self.pointer
        self.pointer += 1

        if self.pointer >= self.len:
            self.pointer = 0
        
        self.deactivate(temp_pointer)
        self.activate()
    
    def down(self) -> None:
        temp_pointer: int = self.pointer
        self.pointer -= 1

        if self.pointer <= -1:
            self.pointer = self.len - 1
        
        self.deactivate(temp_pointer)
        self.activate()
    
    def deactivate(self, temp_pointer: int):
        if self.state == "G":
            self.exGroups[list(self.exGroups)[temp_pointer]].deactivate()
        
        elif self.state == "S":
            self.exGroups[list(self.exGroups)[self.group_pointer]].statments[temp_pointer].deactivate()

        elif self.state == "L":
            self.literar.deactivate(temp_pointer)
    
    def activate(self):
        if self.state == "G":
            self.exGroups[list(self.exGroups)[self.pointer]].activate()
        
        elif self.state == "S":
            self.exGroups[list(self.exGroups)[self.group_pointer]].statments[self.pointer].activate()
        
        elif self.state == "L":
            self.literar.activate(self.pointer)
    
    def confirme_g(self):
        for i in self.exGroups:
            self.exGroups[i].place_forget()

        self.exGroups[list(self.exGroups)[self.pointer]].get_statment_frame([
            exStatment(self.exGroups[list(self.exGroups)[self.pointer]].stframe, exLiterals(self, [("v", "n"), ("1", "d"), ("=", "n"), ("s", "n"), ("/", "n"), ("t", "n")], [[("v", "n"), ("=", "u"), ("s", "u"), ("/", "u"), ("t", "n")], [("v", "n"), ("=", "d"), ("s", "d"), ("/", "d"), ("t", "n")]])),
            exStatment(self.exGroups[list(self.exGroups)[self.pointer]].stframe, exLiterals(self, [("v", "n"), ("2", "d"), ("=", "n"), ("s", "n"), ("/", "n"), ("t", "n")], [[("v", "n"), ("=", "u"), ("s", "u"), ("/", "u"), ("t", "n")], [("v", "n"), ("=", "d"), ("s", "d"), ("/", "d"), ("t", "n")]])),
            exStatment(self.exGroups[list(self.exGroups)[self.pointer]].stframe, exLiterals(self, [("v", "n"), ("3", "d"), ("=", "n"), ("s", "n"), ("/", "n"), ("t", "n")], [[("v", "n"), ("=", "u"), ("s", "u"), ("/", "u"), ("t", "n")], [("v", "n"), ("=", "d"), ("s", "d"), ("/", "d"), ("t", "n")]])),
        ]).place(x = 3, y = 3, relwidth = 0.98, relheight = 0.96)
        
        self.state = "S"
        self.group_pointer = self.pointer
        self.len = len(self.exGroups[list(self.exGroups)[self.pointer]].statments)
        self.pointer = 0
        self.exGroups[list(self.exGroups)[self.group_pointer]].statments[0].activate()
    
    def confirme_s(self) -> None:
        for i in self.exGroups[list(self.exGroups)[self.group_pointer]].statments:
            i.place_forget()
        self.exGroups[list(self.exGroups)[self.group_pointer]].statments[self.pointer].get_lits().place(x = 3, y = 3, relwidth = 0.98, relheight = 0.96)

        self.state = "L"
        self.literar: exLiterals = self.exGroups[list(self.exGroups)[self.group_pointer]].statments[self.pointer].exl
        self.len = len(self.literar.more) + 1
        self.pointer = 0
        self.literar.activate(0)
    
    def enter_l(self):
        ret = [self.literar.main] + self.literar.more
        self.ret = ret[self.pointer]
        
        self.ok()

    def tab(self):
        if self.state == "G": self.confirme_g()
        elif self.state == "S": self.confirme_s()
    
    def enter(self):
        if self.state == "G": self.confirme_g()
        elif self.state == "S": self.confirme_s()
        elif self.state == "L": self.enter_l()

class exGroup(ctk.CTkFrame):
    place_id: int = 0

    def __init__(self, master, title: str, active: bool = False) -> None:
        super().__init__(master=master, fg_color="#000000" if exGroup.place_id % 2 == 1 else "#222222", corner_radius=0)
        self.master = master

        self.place(x = 3, rely = 0.02 + 0.19 * exGroup.place_id, relwidth = 0.98, relheight = 0.19)
        exGroup.place_id += 1

        self.title_lable = ctk.CTkLabel(master=self, text=title)
        self.title_lable.pack(side="left", padx=3)

        self.active_label = ctk.CTkLabel(master=self, text="<-")
        if active: self.active_label.pack(side="right", padx=3)
    
        self.stframe = ctk.CTkFrame(self.master)

    def activate(self) -> None:
        self.active_label.pack(side="right", padx=3)
    
    def deactivate(self) -> None:
        self.active_label.pack_forget()
    
    def get_statment_frame(self, statments: list[exStatment]) -> ctk.CTkFrame:
        self.statments: list[exStatment] = statments

        for index, statment in enumerate(statments):
            statment.place(x = 3, rely = 0.01 + 0.19 * index, relwidth = 0.98, relheight = 0.19)
        
        return self.stframe
        


class exStatment(ctk.CTkFrame):
    place_id: int = 0

    def __init__(self, master, exes: exLiterals):
        super().__init__(master, fg_color="#000000" if exStatment.place_id % 2 == 0 else "#222222")

        self.master = master
        self.line = 0
        self.exl = exes

        self.active_label = ctk.CTkLabel(master=self, text="<-")
        exes.get_main(self, "#000000" if exStatment.place_id % 2 == 0 else "#222222").place(x = 0, y = 0, relwidth = 1, relheight = 1)
        
        exStatment.place_id += 1
    
    def activate(self):
        self.active_label.lift()
        self.active_label.pack(side="right", padx=3)
    
    def deactivate(self):
        self.active_label.pack_forget()
    
    def get_lits(self):
        lits_frame = ctk.CTkFrame(self.master)

        self.exl.create_frame(lits_frame)
        return lits_frame

class exLiterals(ctk.CTkFrame):
    place_id: int = 0

    def __init__(self, master, main: list[tuple[str, str]], more: list[list[tuple[str, str]]]):
        super().__init__(master)

        self.main = main
        self.more = more

        self.normal_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=30)
        self.small_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=17)

    
    def get_main(self, master, fg_color) -> ctk.CTkFrame:
        self.main_frame = ctk.CTkFrame(master, fg_color=fg_color)

        for text, index in self.main:
            ctk.CTkLabel(self.main_frame, text=text, font=self.normal_font if index == "n" else self.small_font, anchor="nw" if index == "u" else "sw" if index == "d" else "w").pack(side = "left")

        return self.main_frame
    
    def create_frame(self, frame):
        self.frames = []
        self.labels = []

        for i, line in enumerate([self.main] + self.more):
            self.line_frame = ctk.CTkFrame(frame)
            self.labels.append(ctk.CTkLabel(master=self.line_frame, text="<-"))
            for text, index in line:
                ctk.CTkLabel(self.line_frame, text=text, font=self.normal_font if index == "n" else self.small_font, anchor="nw" if index == "u" else "sw" if index == "d" else "w").pack(side = "left")
            self.line_frame.place(x = 0, rely = 0.2 * i, relwidth = 1, relheight = 0.2)
            self.frames.append(self.line_frame)
    
    def activate(self, pointer):
        self.labels[pointer].lift()
        self.labels[pointer].pack(side="right", padx=3)
    
    def deactivate(self, pointer):
        self.labels[pointer].pack_forget()