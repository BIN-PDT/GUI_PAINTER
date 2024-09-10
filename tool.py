import customtkinter as ctk
from settings import *


class ToolPanel(ctk.CTkToplevel):
    def __init__(self, parent, binding_color, binding_brush):
        super().__init__(fg_color="white")
        # SETUP.
        self.geometry("250x300")
        self.resizable(False, False)
        self.iconbitmap("images/empty.ico")
        self.attributes("-topmost", True)
        self.title("")
        self.protocol("WM_DELETE_WINDOW", parent.quit)
        # LAYOUT.
        self.rowconfigure(0, weight=2, uniform="A")
        self.rowconfigure(1, weight=3, uniform="A")
        self.rowconfigure((2, 3), weight=1, uniform="A")
        self.columnconfigure((0, 1, 2), weight=1, uniform="A")
        # DATA.
        self.binding_color = binding_color
        self.binding_brush = binding_brush
        # WIDGETS.
        BrushSizeSlider(self, self.binding_brush)
        ColorPanel(self, self.binding_color)


class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent, binding_data):
        super().__init__(master=parent)
        self.grid(row=2, column=0, columnspan=3, sticky=ctk.NSEW, padx=10, pady=5)
        # WIDGET.
        ctk.CTkSlider(master=self, variable=binding_data, from_=0.2, to=1).pack(
            expand=ctk.TRUE, fill=ctk.X, padx=5
        )


class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent, binding_color):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(row=1, column=0, columnspan=3, sticky=ctk.NSEW, padx=10, pady=5)
        # LAYOUT.
        self.rowconfigure(tuple(range(COLOR_ROWS)), weight=1, uniform="A")
        self.columnconfigure(tuple(range(COLOR_COLS)), weight=1, uniform="A")
        # WIDGETS.
        for row in range(COLOR_ROWS):
            for col in range(COLOR_COLS):
                ColorButton(self, row, col, COLORS[row][col], binding_color)


class ColorButton(ctk.CTkButton):
    def __init__(self, parent, row, column, color, binding_color):
        super().__init__(
            master=parent,
            text="",
            corner_radius=3,
            fg_color=f"#{color}",
            hover_color=f"#{color}",
            command=self.apply_color,
        )
        self.grid(row=row, column=column, sticky=ctk.NSEW, padx=1, pady=1)
        # DATA.
        self.original_color = color
        self.binding_color = binding_color

    def apply_color(self):
        self.binding_color.set(self.original_color)
