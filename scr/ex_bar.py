import customtkinter as ctk
import keyboard

data = {
    "Kinematika": {
        (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")): {
            (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")): (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")),
            (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")): (("s", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("v", "n"), (" ", "n"), ("*", "n"), (" ", "n"), ("t", "n")),
            (("t", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("v", "n")): (("v", "n"), (" ", "n"), ("=", "n"), (" ", "n"), ("s", "n"), (" ", "n"), ("/", "n"), (" ", "n"), ("t", "n")),
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
    }
}

class exFrame(ctk.CTkFrame):
    def __init__(self, master, un_show):
        super().__init__(master, border_color="white", border_width=3)
        self.place(x = 150, y = 150, relwidth=0.5, relheight=0.5)
        self.data = data
        self.last_render = exRender(self, self.data, self.next, self.back)
        self.un_show = un_show

    def next(self):
        self.ret = self.last_render.ret
        self.last_render = exRender(self, self.ret, self.next, self.back)
    
    def back(self):
        self.ret = self.last_render.ret
        self.un_show()
    

class exRender(ctk.CTkFrame):
    def __init__(self, master, dato, next_func, back_func):
        super().__init__(master)

        self.data = dato
        self.pointer = 0
        self.temp_pointer = 0
        self.hotkeys = []

        self.frames = []
        self.labels = []

        self.next_func = next_func
        self.back_func = back_func

        self.hotkeys.append(keyboard.add_hotkey("down", self.move_up))
        self.hotkeys.append(keyboard.add_hotkey("up", self.move_down))
        self.hotkeys.append(keyboard.add_hotkey("tab", self.ret_t))
        self.hotkeys.append(keyboard.add_hotkey("enter", self.ret_e))

        self.normal_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=30)
        self.small_font: ctk.CTkFont = ctk.CTkFont(family="Consolas", size=17)

        for num, i in enumerate(self.data):
            frame = ctk.CTkFrame(self)

            if isinstance(i, str):
                ctk.CTkLabel(frame, text=i).pack(side="left")
            
            else:
                for letter, index in i:
                    ctk.CTkLabel(frame, text=letter, font=self.normal_font if index == "n" else self.small_font, anchor="w" if index == "n" else "nw" if index == "u" else "sw").pack(side="left")
            
            label = ctk.CTkLabel(frame, text="<-")

            self.frames.append(frame)
            self.labels.append(label)
            frame.place(x = 0, y = 0 + 30 * num, relwidth=1, relheight=0.2)
        
        self.place(x = 3, y = 3, relwidth=0.98, relheight=0.96)

    def move_up(self):
        self.pointer += 1

        if len(list(self.data)) <= self.pointer:
            self.pointer = 0
        
        self.activate()

    def move_down(self):
        self.pointer -= 1

        if self.pointer == -1:
            self.pointer = len(list(self.data)) - 1
            # print(self.data)
        
        self.activate()
    
    def activate(self):
        self.labels[self.pointer].pack(side="right")
        self.labels[self.temp_pointer].pack_forget()

        self.temp_pointer = self.pointer
    
    def ret_t(self):
        self.ret = self.data[list(self.data)[self.pointer]]

        for i in self.hotkeys:
            keyboard.remove_hotkey(i)
        
        self.next_func() if not isinstance(self.ret, tuple) else self.back_func()
    
    def ret_e(self):
        self.ret = self.data[list(self.data)[self.pointer]]

        for i in self.hotkeys:
            keyboard.remove_hotkey(i)

        self.next_func() if not isinstance(self.ret, tuple) else self.back_func()