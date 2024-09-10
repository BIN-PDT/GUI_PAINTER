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
        ColorSliderPanel(self, self.binding_color)


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


class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, binding_color):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=10, pady=5)
        # LAYOUT.
        self.rowconfigure((0, 1, 2), weight=1, uniform="A")
        self.columnconfigure(0, weight=1, uniform="A")
        # DATA.
        self.color_RGB = binding_color
        self.color_R = ctk.IntVar(value=binding_color.get()[0])
        self.color_G = ctk.IntVar(value=binding_color.get()[1])
        self.color_B = ctk.IntVar(value=binding_color.get()[2])
        self.color_RGB.trace_add("write", self.set_color)
        # WIDGETS.
        self.load_slider(0, 0, "R", SLIDER_R, self.color_R)
        self.load_slider(1, 0, "G", SLIDER_G, self.color_G)
        self.load_slider(2, 0, "B", SLIDER_B, self.color_B)

    def load_slider(self, row, column, component, color, binding_data):
        ctk.CTkSlider(
            master=self,
            button_color=color,
            button_hover_color=color,
            from_=0,
            to=15,
            number_of_steps=16,
            variable=binding_data,
            command=lambda value: self.set_component_color(component, value),
        ).grid(row=row, column=column, padx=5, pady=5)

    def set_component_color(self, component, value):
        color = list(self.color_RGB.get())
        match component:
            case "R":
                color[0] = COLOR_RANGE[int(value)]
            case "G":
                color[1] = COLOR_RANGE[int(value)]
            case "B":
                color[2] = COLOR_RANGE[int(value)]
        self.color_RGB.set("".join(color))

    def set_color(self, *args):
        color = tuple(self.color_RGB.get())
        self.color_R.set(COLOR_RANGE.index(color[0]))
        self.color_G.set(COLOR_RANGE.index(color[1]))
        self.color_B.set(COLOR_RANGE.index(color[2]))
