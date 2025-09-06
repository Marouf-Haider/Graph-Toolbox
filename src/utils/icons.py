from enum import Enum
from PIL import Image
import customtkinter as ctk
import os

ICON_DIR = "assets/icons"

class IconName(Enum):
    PLOT_2D = "2d_plot"
    PLOT_3D = "3d_plot"
    CALCULATOR = "calculator"
    EDIT = "edit"
    LEFT = "left"
    LIGHT_MODE = "light_mode"
    LIST = "list"
    REMOVE = "remove"
    RIGHT = "right"
    SAVE = "save"
    SETTINGS = "settings"
    GITHUB = 'github'
    RESET = 'reset'
    SELECT_ALL ='select_all'
    COMPLEX = 'complex'
def get_icon(icon: IconName, width: int) -> ctk.CTkImage:

    name = icon.value
    dark_path = os.path.join(ICON_DIR, "dark", f"{name}.png")
    light_path = os.path.join(ICON_DIR, "light", f"{name}.png")

    icon_obj = ctk.CTkImage(
        dark_image=Image.open(dark_path),
        light_image=Image.open(light_path),
        size=(width, width)
    )
    return icon_obj
