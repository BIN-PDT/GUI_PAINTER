import customtkinter as ctk
from settings import *


class Canvas(ctk.CTkCanvas):
    def __init__(self, parent):
        super().__init__(
            master=parent,
            background=CANVAS_BG,
            bd=0,
            highlightthickness=0,
            relief=ctk.RIDGE,
        )
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)
