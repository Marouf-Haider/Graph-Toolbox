import customtkinter as ctk
import webbrowser
from tkinter import messagebox

from src.utils import *
from src.ui.grapher_2d import Grapher_2D

class Home(ctk.CTk):
    def __init__(self, fg_color = None, **kwargs):
        super().__init__(fg_color, **kwargs)
        self._2d_grapher = None
        self._3d_grapher = None
        self.parametric_grapher = None

        self.setup_window()
        self._build_widgets()

    def setup_window(self):
        # Configure window
        self.iconbitmap("assets\\icons\\app_icon.ico")
        self.title("Graphing tools")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.width =int(screen_width*0.8)
        self.height = int(screen_height*0.8)

        x = int((screen_width - self.width) / 2)
        y = int((screen_height - self.height) / 2)

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.minsize(self.width,self.height)
        self.resizable(False, False)



    def _build_widgets(self):

        self.top_label = ctk.CTkLabel(self,text= 'Graphing toolbox\n by Haider Marouf',font = ("Roboto",32,'bold'))
        self.top_label.pack(side= 'top', padx=10,pady =30, fill ='x', expand =False)

        self.frame = ctk.CTkFrame(self)
        self.frame.pack(expand = True, fill = 'both', padx = 30, pady = 30)

        self.frame.grid_columnconfigure((0,2), weight=1)
        self.frame.grid_rowconfigure((0,1), weight=1)



        self._2d_graph_button = ctk.CTkButton(self.frame, text = '2D\n Graph',
                                              font = ("Roboto",20,'bold'),
                                              image= get_icon(IconName.PLOT_2D,140),
                                              compound ='left',
                                              command = self.open_2d_grapher,
                                              anchor='center',
                                              )
        #self._2d_graph_button.pack(expand = False, fill = 'both', padx = 15, pady = 15)
        self._2d_graph_button.grid(row=0, column=0, sticky = 'nsew', padx = 35, pady = 35)

        self._3d_graph_button = ctk.CTkButton(self.frame, text = '3D Graph',
                                                font = ("Roboto",20,'bold'),
                                                image= get_icon(IconName.PLOT_3D,140),
                                                compound= 'left',
                                                command = self.open_3d_grapher,
                                                anchor='center',
                                              )
        #self._3d_graph_button.pack(expand = False, fill = 'both', padx = 35, pady = 35)
        self._3d_graph_button.grid(row=0, column=1,sticky = 'nsew', padx = 35, pady = 35)

        self.parametric_graph_button = ctk.CTkButton(self.frame, text = 'Parametric\n Graph',
                                                    font = ("Roboto",20,'bold'),
                                                    image= get_icon(IconName.PLOT_2D,140),
                                                    compound= 'left',
                                                    command= self.open_parametric_grapher,
                                                    anchor='center',
                                                    )
        #self.parametric_graph_button.pack(expand = False, fill = 'both', padx = 35, pady = 35)
        self.parametric_graph_button.grid(row=0, column=2,sticky = 'nsew', padx = 35, pady = 35)

        self.complex_graph_button = ctk.CTkButton(self.frame, text = 'Complex\n Graph',
                                                    font = ("Roboto",20,'bold'),
                                                    image= get_icon(IconName.COMPLEX,140),
                                                    compound= 'left',
                                                    command= self.open_parametric_grapher,
                                                    anchor='center',
                                                    )
        #self.parametric_graph_button.pack(expand = False, fill = 'both', padx = 35, pady = 35)
        self.complex_graph_button.grid(row=1, column=0,sticky = 'nsew', padx = 35, pady = 35)

        self.github_button = ctk.CTkButton(self.frame, text = 'Github',
                                                    font = ("Roboto",20,'bold'),
                                                    image= get_icon(IconName.GITHUB,140),
                                                    compound= 'left',
                                                    command= self.github_button_callback,
                                                    anchor='center',
                                                    )
        #self.parametric_graph_button.pack(expand = False, fill = 'both', padx = 35, pady = 35)
        self.github_button.grid(row=1, column=1,sticky = 'nsew', padx = 35, pady = 35)
        
        self.parameters_button = ctk.CTkButton(self.frame, text = 'Parameters',
                                                     font = ("Roboto",20,'bold'),
                                                     image=get_icon(IconName.SETTINGS,140),
                                                     compound='left',
                                                     anchor='center',
                                                     
                                                     )

        self.parameters_button.grid(row=1, column=2,sticky = 'nsew', padx = 35, pady = 35)


 
        
    def open_2d_grapher(self):
        if self._2d_grapher is None or not self._2d_grapher.winfo_exists():
            self._2d_grapher = Grapher_2D(parent = self)  # create window if its None or destroyed
            self._2d_grapher.lift()  # Bring to front
            self._2d_grapher.focus_force()  # Force focus
            self._2d_grapher.grab_set()  # Make it modal (optional)
        else:
            self._2d_grapher.lift()  # Bring to front
            self._2d_grapher.focus_force()  # Force focus  
        return

    def open_3d_grapher(self):
        messagebox.showinfo('Info', 'This feature will be available soon.')
        return
    def open_parametric_grapher(self):
        messagebox.showinfo('Info', 'This feature will be available soon.')
        return  
    def github_button_callback(self):
        webbrowser.open("https://github.com/Marouf-Haider")
