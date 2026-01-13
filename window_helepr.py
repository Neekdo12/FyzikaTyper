import customtkinter as ctk

from window import Window

class WindowLink(ctk.CTkFrame):
    def __init__(self, master, window: Window, title: str = "Undefined title") -> None:
        super().__init__(master=master, fg_color="#161414")
        self.window: Window = window
        self.title = title

        self.label = ctk.CTkLabel(self, text=title)
        self.label.pack(ipadx = 10, ipady = 1)
    
    def render(self) -> None:
        self.window.place(x = 0, rely = 0.1, relwidth = 1, relheight = 0.9)
    
    def clear(self) -> None:
        self.window.place_forget()
    
    def remove(self):
        self.pack_forget()
        self.window.place_forget()
        
class WindowSwitcher(ctk.CTkScrollableFrame):
    id: int = 0

    def __init__(self, master) -> None:
        super().__init__(master=master, orientation="horizontal", corner_radius=0, fg_color="#000000")
        self._scrollbar.configure(height = 5)

        self.a_window: str = ""
        self.windows: dict[str, WindowLink] = {}

        self.place(x = 0, y = 0, relwidth = 1, relheight = 0.1)
    
    def add_window(self, window_link: WindowLink, main = False) -> None:
        window_link.label.bind("<Button-1>", self.set_window(window_link.title))
        window_link.bind("<Button-1>", self.set_window(window_link.title))

        self.windows[window_link.title] = window_link
        window_link.pack(side = "left", fill = "y", expand = True, padx = 2, pady = 1)

        if main or not self.a_window:
            self.a_window = window_link.title
            window_link.render()

    def set_window(self, window: str):
        def run(event):
            try:
                self.windows[self.a_window].clear()
            except KeyError:
                print("Window no longer exists")
                
            self.a_window = window
            self.windows[self.a_window].render()
        
        return run

    def active_window(self) -> Window:
        return self.windows[self.a_window].window

    def remove_window(self, name: str):
        self.windows.pop(name).remove()