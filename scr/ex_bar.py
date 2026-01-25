from ctypes import pointer
import customtkinter as ctk
import keyboard

data = {
    "Kinematika": {
        (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")): {
            (("v", "n"), ("0", "d"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), ("A", "d"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n"), ("c", "d"), ("v", "n"), ("1", "d"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), ("A", "d"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n"), ("c", "d")): (("v", "n"), ("0", "d"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), ("A", "d"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n"), ("c", "d"), ("v", "n"), ("1", "d"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), ("B", "d"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n"), ("B", "d")),
            (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")): (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")),
            (("t", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("v", "n")): (("t", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    },
    "Dynamika": {
        (("v", "n"), ("=", "n"), ("v", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    },
    "Astrofyzika": {
        (("v", "n"), ("=", "n"), ("v", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    },
    "Kinematika2": {
        (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")): {
            (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")): (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")),
            (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")): (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")),
            (("t", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("v", "n")): (("t", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    },
    "Dynamika2": {
        (("v", "n"), ("=", "n"), ("v", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    },
    "Astrofyzika2": {
        (("v", "n"), ("=", "n"), ("v", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("a", "n"), ("=", "n"), ("a", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        },
        (("b", "n"), ("=", "n"), ("b", "n")): {
            (("1", "n"), ("=", "n"), ("v", "n")): (("1", "n"), ("=", "n"), ("v", "n")),
            (("2", "n"), ("=", "n"), ("v", "n")): (("2", "n"), ("=", "n"), ("v", "n")),
            (("3", "n"), ("=", "n"), ("v", "n")): (("3", "n"), ("=", "n"), ("v", "n")),
        }
    }
}

class exFrame(ctk.CTkFrame):
    def __init__(self, master, un_show):
        super().__init__(master, border_color="white", border_width=3)
        self.place(relx = 0.5, rely = 0.5, relwidth=0.5, relheight=0.5, anchor = "center")
        self.data = data
        self.last_render = exRender(self, self.data, self.next, self.back, self.set, self.end)
        self.un_show = un_show

    def next(self):
        self.ret = self.last_render.ret
        self.last_render = exRender(self, self.ret, self.next, self.back, self.set, self.end)
    
    def back(self):
        self.ret = self.last_render.ret
        self.un_show()
    
    def set(self):
        self.ret = self.last_render.ret
        self.last_render = exSetter(self, self.back, self.ret)

    def end(self):
        self.ret = []
        self.un_show()

class exSetter(ctk.CTkFrame):
    def __init__(self, master, back, data):
        super().__init__(master=master)

        self.columnconfigure((0, 1), weight=1, uniform="a")
        self.rowconfigure((0, 1, 2, 3), weight=1, uniform="a")

        self.ret = data
        self.data = data
        self.back = back
        self.names = {}
        self.last = "n"
        self.name = ""

        self.normal_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=30)
        self.small_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=17)

        self.frame = ctk.CTkFrame(self, fg_color="transparent")
        self.texts = []

        self.frames = []

        for letter, index in self.data:
            self.texts.append(ctk.CTkLabel(self.frame, text=letter, font=self.normal_font if index == "n" else self.small_font, anchor="w" if index == "n" else "nw" if index == "u" else "sw"))
            self.texts[-1].pack(side="left")

        self.frame.grid(column=0, row=0, columnspan=2,pady = 3)

        for letter, index in self.data:
            if index == "d":
                if self.last == "d":
                    self.name += letter
                else:
                    self.last = "d"
                    self.name = letter
            
            elif index == "n" and self.last == "d":
                self.names[self.name] = None
                self.last = "n"
        
        if self.last == "d":
            self.names[self.name] = None
        
        for row, name in enumerate(self.names):
            frame = ctk.CTkFrame(self, fg_color="transparent")
            self.frames.append(frame)

            var = ctk.StringVar(self, "")
            ctk.CTkLabel(frame, text=f"{name}:", font=self.normal_font).pack(side = "left", padx = 3)
            entry = ctk.CTkEntry(frame, textvariable=var)
            entry.pack(side = "right", padx=3)

            if row == 0: entry.focus()

            self.names[name] = var
            column = 0 if row < 3 else 1
            row = row + 1 if row < 3 else row - 2
            frame.grid(row = row, column = column,pady = 3)


        self.place(x = 3, y = 3, relwidth=0.98, relheight=0.96)
        self.short_cut = keyboard.add_hotkey("return", self.end)
    
    def end(self):
        keyboard.remove_hotkey(self.short_cut)

        for i in self.names:
            if self.names[i].get() == "":
                self.names[i].set(i)
            
            self.names[i] = self.names[i].get()
            ret = []

            for index in self.names[i]:
                ret.append((index, "d"))
            
            self.names[i] = ret
        
        self.ret = []
        self.name = ""
        self.last = "n"
        
        for letter, index in self.data:
            if index != "d":
                if self.last == "d":
                    for i in self.names[self.name]:
                        self.ret.append(i)

                self.ret.append((letter, index))
                self.last = "n"
            
            else:
                if self.last == "d":
                    self.name += letter
                else:
                    self.name = letter
                    print(letter, self.name)

                self.last = "d"
        if self.last == "d":
            for i in self.names[self.name]:
                self.ret.append(i)
        
        self.back()

class exRender(ctk.CTkFrame):
    def __init__(self, master, dato, next_func, back_func, set_func, end):
        super().__init__(master)

        self.data = dato
        self.pointer = 0
        self.temp_pointer = 0
        self.hotkeys = []

        self.frames = []
        self.labels = []
        self.texts = []

        self.next_func = next_func
        self.back_func = back_func
        self.set_func = set_func
        self.end_func = end

        self.hotkeys.append(keyboard.add_hotkey("down", self.move_up))
        self.hotkeys.append(keyboard.add_hotkey("up", self.move_down))
        self.hotkeys.append(keyboard.add_hotkey("tab", self.ret_t))
        self.hotkeys.append(keyboard.add_hotkey("enter", self.ret_e))
        self.hotkeys.append(keyboard.add_hotkey("esc", self.end))

        self.normal_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=30)
        self.small_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=17)

        for num, i in enumerate(self.data):
            frame = ctk.CTkFrame(self)

            if isinstance(i, str):
                self.texts.append(ctk.CTkLabel(frame, text=i))
                self.texts[-1].pack(side="left")
            
            else:
                for letter, index in i:
                    self.texts.append(ctk.CTkLabel(frame, text=letter, font=self.normal_font if index == "n" else self.small_font, anchor="w" if index == "n" else "nw" if index == "u" else "sw"))
                    self.texts[-1].pack(side="left")
            
            label = ctk.CTkLabel(frame, text="<-")

            self.frames.append(frame)
            self.labels.append(label)
            frame.place(x = 0, y = 0 + 30 * num, relwidth=1, relheight=0.2)
        
        self.place(x = 3, y = 3, relwidth=0.98, relheight=0.96)
        self.activate()

    def move_up(self):
        self.pointer += 1

        if len(list(self.data)) <= self.pointer:
            self.pointer = 0
        
        self.scroll()
        self.activate()

    def move_down(self):
        self.pointer -= 1

        if self.pointer == -1:
            self.pointer = len(list(self.data)) - 1
        
        self.scroll()
        self.activate()
    
    def activate(self):
        self.labels[self.temp_pointer].pack_forget()
        self.labels[self.pointer].pack(side="right")

        self.temp_pointer = self.pointer
    
    def ret_t(self):
        self.ret = self.data[list(self.data)[self.pointer]]

        for i in self.hotkeys:
            keyboard.remove_hotkey(i)
        
        if not isinstance(self.ret, tuple):
            self.next_func()
        else:
            self.set_func()
    
    def ret_e(self):
        self.ret = self.data[list(self.data)[self.pointer]]

        for i in self.hotkeys:
            keyboard.remove_hotkey(i)

        try:
            if isinstance(self.ret[list(self.ret)[0]], tuple):
                self.ret = list(self.ret)[0]
                self.back_func()
                return None
        except TypeError:
            ...

        if not isinstance(self.ret, tuple):
            self.next_func()
        else:
            self.back_func()
    
    def end(self):
        for i in self.hotkeys:
            keyboard.remove_hotkey(i)

        self.end_func()
    
    def scroll(self):
        if self.pointer >= 5 or self.pointer == 0:
            for i in self.texts:
                i.pack_forget()

            self.texts.clear()
            self.frames.clear()
            self.labels.clear()

            offset = (self.pointer - 4) * 30 if self.pointer != 0 else 0

            for num, i in enumerate(self.data):
                frame = ctk.CTkFrame(self)

                if isinstance(i, str):
                    self.texts.append(ctk.CTkLabel(frame, text=i))
                    self.texts[-1].pack(side="left")
                
                else:
                    for letter, index in i:
                        self.texts.append(ctk.CTkLabel(frame, text=letter, font=self.normal_font if index == "n" else self.small_font, anchor="w" if index == "n" else "nw" if index == "u" else "sw"))
                        self.texts[-1].pack(side="left")
                
                label = ctk.CTkLabel(frame, text="<-")

                self.frames.append(frame)
                self.labels.append(label)
                frame.place(x = 0, y = 0 + 30 * num - offset, relwidth=1, relheight=0.2)