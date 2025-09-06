#!.\.venv\Scripts\python.exe

import customtkinter as ctk
from src.ui.home import Home


if __name__ == "__main__":
    ctk.set_appearance_mode("dark")  
    ctk.set_default_color_theme('dark-blue')

    app = Home()
    app.mainloop()

    
