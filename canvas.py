import customtkinter as ctk
from settings import *


class Canvas(ctk.CTkCanvas):
    def __init__(self, parent, binding_color, binding_brush):
        super().__init__(
            master=parent,
            background=CANVAS_BG,
            bd=0,
            highlightthickness=0,
            relief=ctk.RIDGE,
        )
        self.pack(expand=ctk.TRUE, fill=ctk.BOTH)
        # DATA.
        self.binding_color = binding_color
        self.binding_brush = binding_brush
        self.allow_draw = False
        self.old_x = self.old_y = None
        # EVENT.
        self.bind("<Motion>", self.draw)
        self.bind("<Button>", self.activate)
        self.bind("<ButtonRelease>", self.deactivate)

    def draw(self, event):
        if self.allow_draw:
            if self.old_x and self.old_y:
                self.line((self.old_x, self.old_y), (event.x, event.y))
            self.old_x, self.old_y = event.x, event.y

    def activate(self, event):
        self.allow_draw = True
        self.line((event.x, event.y), (event.x, event.y))

    def deactivate(self, event):
        self.allow_draw = False
        self.old_x = self.oldy = None

    def line(self, src, des):
        width = self.binding_brush.get() * BRUSH_RATIO
        color = f"#{self.binding_color.get()}"
        self.create_line(src, des, width=width, capstyle=ctk.ROUND, fill=color)
