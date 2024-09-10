import customtkinter as ctk
from PIL import Image
from settings import *


class ToolPanel(ctk.CTkToplevel):
    def __init__(
        self, parent, binding_color, binding_brush, binding_erase, clear_canvas
    ):
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
        self.binding_erase = binding_erase
        # WIDGETS.
        BrushSizeSlider(self, self.binding_brush)
        ColorPanel(self, self.binding_color, self.binding_erase)
        ColorSliderPanel(self, self.binding_color, self.binding_erase)
        BrushButton(self, self.binding_erase)
        EraseButton(self, self.binding_erase)
        ClearButton(self, self.binding_erase, clear_canvas)
        # SET DEFAULT CHOICE.
        self.binding_erase.set(False)


class BrushSizeSlider(ctk.CTkFrame):
    def __init__(self, parent, binding_data):
        super().__init__(master=parent)
        self.grid(row=2, column=0, columnspan=3, sticky=ctk.NSEW, padx=10, pady=5)
        # WIDGET.
        ctk.CTkSlider(master=self, variable=binding_data, from_=0.2, to=1).pack(
            expand=ctk.TRUE, fill=ctk.X, padx=5
        )


class ColorPanel(ctk.CTkFrame):
    def __init__(self, parent, binding_color, binding_erase):
        super().__init__(master=parent, fg_color="transparent")
        self.grid(row=1, column=0, columnspan=3, sticky=ctk.NSEW, padx=10, pady=5)
        # LAYOUT.
        self.rowconfigure(tuple(range(COLOR_ROWS)), weight=1, uniform="A")
        self.columnconfigure(tuple(range(COLOR_COLS)), weight=1, uniform="A")
        # WIDGETS.
        for row in range(COLOR_ROWS):
            for col in range(COLOR_COLS):
                color = COLORS[row][col]
                ColorButton(self, row, col, color, binding_color, binding_erase)


class ColorButton(ctk.CTkButton):
    def __init__(self, parent, row, column, color, binding_color, binding_erase):
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
        self.binding_erase = binding_erase

    def apply_color(self):
        self.binding_color.set(self.original_color)
        self.binding_erase.set(False)


class ColorSliderPanel(ctk.CTkFrame):
    def __init__(self, parent, binding_color, binding_erase):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky=ctk.NSEW, padx=10, pady=5)
        # LAYOUT.
        self.rowconfigure((0, 1, 2), weight=1, uniform="A")
        self.columnconfigure(0, weight=1, uniform="A")
        # DATA.
        self.binding_erase = binding_erase
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
        self.binding_erase.set(False)
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


class Button(ctk.CTkButton):
    def __init__(self, parent, column, image, command):
        super().__init__(
            master=parent,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER_COLOR,
            text="",
            image=ctk.CTkImage(image, image),
            command=command,
        )
        self.grid(row=3, column=column, sticky=ctk.NSEW, padx=10, pady=5)


class BrushButton(Button):
    def __init__(self, parent, binding_erase):
        super().__init__(
            parent=parent,
            column=0,
            image=Image.open("images/ui/brush.png"),
            command=self.activate,
        )
        # DATA.
        self.binding_erase = binding_erase
        self.binding_erase.trace_add("write", self.update_state)

    def activate(self):
        self.binding_erase.set(False)

    def update_state(self, *args):
        color = BUTTON_COLOR if self.binding_erase.get() else BUTTON_ACTIVE_COLOR
        self.configure(fg_color=color)


class EraseButton(Button):
    def __init__(self, parent, binding_erase):
        super().__init__(
            parent=parent,
            column=1,
            image=Image.open("images/ui/eraser.png"),
            command=self.activate,
        )
        # DATA.
        self.binding_erase = binding_erase
        self.binding_erase.trace_add("write", self.update_state)

    def activate(self):
        self.binding_erase.set(True)

    def update_state(self, *args):
        color = BUTTON_ACTIVE_COLOR if self.binding_erase.get() else BUTTON_COLOR
        self.configure(fg_color=color)


class ClearButton(Button):
    def __init__(self, parent, binding_erase, clear_canvas):
        super().__init__(
            parent=parent,
            column=2,
            image=Image.open("images/ui/clear.png"),
            command=self.activate,
        )
        # DATA.
        self.binding_erase = binding_erase
        self.clear_canvas = clear_canvas

    def activate(self):
        self.binding_erase.set(False)
        self.clear_canvas()
