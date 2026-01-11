import customtkinter as ctk

from window import Window

class WindowSwitcher(ctk.CTkScrollableFrame):
    def __init__(self, master) -> None:
        super().__init__(master=master, orientation="horizontal", corner_radius=0, fg_color="#000000")
        self._scrollbar.configure(height = 5)

        self.a_window: int = 0
        self.windows: list[WindowLink] = []

        self.place(x = 0, y = 0, relwidth = 1, relheight = 0.1)
    
    def add_window(self, window_link: WindowLink, main = False) -> None:
        self.windows.append(window_link)
        window_link.pack(side = "left", fill = "y", expand = True, padx = 2, pady = 1)

        if main:
            self.a_window = len(self.windows) - 1
            window_link.render()

    def set_window(self, window: int):
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
        super().__init__(master=master, fg_color="#161414")
        self.window: Window = window
        self.title = title

        self.label = ctk.CTkLabel(self, text=title)
        self.label.pack(ipadx = 10, ipady = 1)

        self.label.bind("<Button-1>", master.set_window(WindowLink.id))
        self.bind("<Button-1>", master.set_window(WindowLink.id))
        WindowLink.id += 1
    
    def render(self) -> None:
        self.window.place(x = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
    
    def clear(self) -> None:
        self.window.place_forget()