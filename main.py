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
        # WIDGET.
        Canvas(self)


if __name__ == "__main__":
    App().mainloop()
