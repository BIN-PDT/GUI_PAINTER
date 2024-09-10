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
        self.erase = ctk.BooleanVar()
        # WIDGET.
        self.canvas = Canvas(self, self.color, self.brush, self.erase)
        ToolPanel(self, self.color, self.brush, self.erase, self.clear_canvas)
        # EVENT.
        self.bind("<MouseWheel>", self.resize_brush)

    def resize_brush(self, event):
        size = self.brush.get() + 0.05 * int(event.delta / abs(event.delta))
        self.brush.set(max(0.2, min(1, size)))

    def clear_canvas(self):
        self.canvas.delete(ctk.ALL)


if __name__ == "__main__":
    App().mainloop()
