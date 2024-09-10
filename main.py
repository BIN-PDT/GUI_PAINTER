import customtkinter as ctk
from settings import *
from canvas import Canvas
from tool import ToolPanel


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
        ToolPanel(self, self.color, self.brush)
        # EVENT.
        self.bind("<MouseWheel>", self.resize_brush)

    def resize_brush(self, event):
        size = self.brush.get() + 0.05 * int(event.delta / abs(event.delta))
        self.brush.set(max(0.2, min(1, size)))


if __name__ == "__main__":
    App().mainloop()
