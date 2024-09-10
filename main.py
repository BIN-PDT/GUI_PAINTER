import customtkinter as ctk
from settings import *
from canvas import Canvas


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        # SETUP.
        ctk.set_appearance_mode("light")
        self.geometry("800x600")
        self.iconbitmap("images/empty.ico")
        self.title("")
        # DATA.
        self.color = ctk.StringVar(value="000")
        self.brush = ctk.DoubleVar(value="0.2")
        # WIDGET.
        Canvas(self, self.color, self.brush)


if __name__ == "__main__":
    App().mainloop()
