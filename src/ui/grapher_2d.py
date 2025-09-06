import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.ticker import MaxNLocator
from tkinter import messagebox, filedialog 
from CTkColorPicker import *

from src.utils.icons import get_icon, IconName
from src.ui.function_window import FunctionWindow 

class Grapher_2D(ctk.CTkToplevel):
    def __init__(self, parent =None,*args, **kwargs):
        super().__init__(master = parent,*args, **kwargs)


        # important variables:
        self.parent = parent
        self.current_theme = ctk.StringVar(value='light')
        self.plot_theme    = ctk.StringVar(value ='default')

        self.setup_window()
        self.initialize_variables()
        
        self.create_widgets()
        self.bind_events()
    def setup_window(self):
        # Configure window
        self.iconbitmap("assets\\icons\\app_icon.ico")
        self.title("2D Graph visualiser")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        
        self.width =int(screen_width*0.8)
        self.height = int(screen_height*0.8)

        x = int((screen_width - self.width) / 2)
        y = int((screen_height - self.height) / 2)

        self.geometry(f"{self.width}x{self.height}+{x}+{y}")
        self.minsize(self.width,self.height)

        # Configure the main grid 
        self.grid_columnconfigure(0, weight = 1)
        self.grid_columnconfigure(1, weight = 2)
        self.grid_rowconfigure(0, weight= 0)
        self.grid_rowconfigure(1, weight= 1)

    def initialize_variables(self):
        self.function_window = None
        self.left_frame_visible = True      
        self.functions = []
        self.legend_state = ctk.StringVar(value ='off')
        self.grid_state   = ctk.StringVar(value ='off')


    def _build_left_frame(self):
        # Left frame
        self.left_frame = ctk.CTkFrame(self)
        self.left_frame.grid(column = 0,row =1, sticky ='nsew',padx =5, pady =5, ipadx= 0)


        # functions frame
        self.functions_frame = ctk.CTkScrollableFrame(self.left_frame,
                                                        label_text='Functions ',
                                                        
                                                        label_font=("Roboto",16, "bold", "roman"),
                                                    )
        self.functions_frame.pack(side ='top',padx=10, pady = 10, fill ='x')
        self.functions_frame._scrollbar.grid_remove()
        # button frame 
        self.buttons_frame = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        self.buttons_frame.pack(padx =10,pady=10, 
                                fill =ctk.BOTH
                            )
        self.buttons_frame.columnconfigure((0,1,2,3), weight=1)
        self.buttons_frame.rowconfigure(0, weight=1)
        # Add function button
        self.add_function_button = ctk.CTkButton(self.buttons_frame, 
                                    text="Add",
                                    font = ("Roboto",16),
                                      command = self.open_function_window)
    
        self.add_function_button.grid(column =0, row =0, padx = 5, pady =5) 
        # select deselect all button
        self.select_all_button = ctk.CTkButton(self.buttons_frame, 
                                                        text ='',
                                                        image= get_icon(IconName.SELECT_ALL,24),
                                                        font = ("Roboto",16),
                                                        command = self.select_all
                                                        )
        self.select_all_button.grid(column =1, row =0, padx =5, pady =5)
        # Plot button
        self.plot_button = ctk.CTkButton(self.buttons_frame,
                                          text="Plot", 
                                          font = ("Roboto",16),
                                          command = self.plot)
        self.plot_button.grid(column =2, row =0, padx = 5, pady =5)
        # Remove button
        self.remove_button = ctk.CTkButton(self.buttons_frame,
                                            text="",
                                             font = ("Roboto",16),
                                             image= get_icon(IconName.REMOVE,24),
                                            command = self.remove)
        self.remove_button.grid(column =3, row =0, padx = 5, pady =5)

        # resolution frame 
        self.resolution_frame = ctk.CTkFrame(self.left_frame)
        self.resolution_frame.pack(padx =10,pady=10, 
                                fill =ctk.BOTH                         
                                )
        # slider label
        self.slider_label = ctk.CTkLabel(self.resolution_frame,
                                        text= f'Resolution:',
                                        font= ("Roboto",16, "bold", "roman") 
                                        )
        self.slider_label.pack(side ='left',pady=0, padx= 5, expand=True)   

        # Number of points slider
        self.resolution_slider = ctk.CTkSlider(self.resolution_frame, 
                                    from_ = 50,
                                    to = 500, 
                                    command = self.slide
                                        )
        self.resolution_slider.pack(pady=0, padx=5 ,expand=True, fill ='x')
        self.resolution_slider.set(100)

        
        # save frame
        self.save_frame = ctk.CTkFrame(self.left_frame, fg_color='transparent')
        self.save_frame.pack(padx =10, pady =10, fill ='both')
        # Save button label
        self.save_button = ctk.CTkButton(self.save_frame, 
                                    text="Save",
                                    font= ("Roboto",16, "bold", "roman"),
                                    height=50,
                                    image=get_icon(IconName.SAVE,24),
                                    compound='right',
                                    command=self.save_callback
                                    )
        self.save_button.pack(padx=5,pady=5, side = 'right', expand =True, fill= 'y')
        # Save button
        self.save_options = ctk.CTkSegmentedButton(self.save_frame, 
                                                  values= ['PNG','JPG','PDF','SVG'],
                                                  dynamic_resizing=True
                                                  )
        self.save_options.pack(side='left',padx=5, pady=5, expand =True,fill = 'both')
        self.save_options.set('PNG')



    def _build_top_frame(self):
        # Top right frame
        self.top_frame = ctk.CTkFrame(self)
        self.top_frame.grid(column= 0,row =0, columnspan =2, stick ='nsew', padx = 5,pady =5) 
        # Toggle button for left frame
        self.toggle_button = ctk.CTkButton(self.top_frame, 
                                     text="",
                                     fg_color='transparent',
                                     hover=False,
                                     image=get_icon(IconName.LEFT,40),
                                     width= 20,
                                     font= ("Roboto",25, "bold"),
                                     command=self.toggle_left_frame
                                     )
        self.toggle_button.pack(side='left', pady=10, padx= 5)  
        # Reset-all button
        self.reset_button = ctk.CTkButton(self.top_frame, 
                                    text="Reset",
                                    image= get_icon(IconName.RESET,16),
                                      command = self.reset_all,
                                      fg_color="#FF9100",
                                      hover_color="#A85F01"
                                    )
        self.reset_button.pack(side= 'left',pady=10, padx=5 )
        # Theme switch
        self.theme_switch = ctk.CTkButton(self.top_frame, 
                                          text ='',
                                        font= ("Roboto",25),
                                        text_color='black',
                                        fg_color='transparent',
                                        image= get_icon(IconName.LIGHT_MODE,32),
                                        hover = False,
                                        command = self.switch_theme,
                                        width=40
                                          )
        self.theme_switch.pack(side = 'right', padx = 5,pady =10)
        # plot theme modes toggle
        self.plot_theme_options = ctk.CTkOptionMenu(self.top_frame, 
                                        values = plt.style.available,
                                        variable = self.plot_theme,
                                        font= ("Roboto",18, "bold", "roman"),
                                        )
        
        self.plot_theme_options.pack(side = 'left', pady = 10, padx= 5)
        self.plot_theme_options.set("default")

        # Grid switch
        self.grid_switch = ctk.CTkSwitch(self.top_frame, text= 'Grid',                                
                                        variable = self.grid_state,
                                        onvalue  = 'on',
                                        offvalue = 'off',
                                        )
        self.grid_switch.pack(side = 'left', pady = 10, padx= 5)


        # legend switch
        self.legend_switch = ctk.CTkSwitch(self.top_frame, text= 'Legend',                                
                                        variable = self.legend_state,
                                        onvalue  = 'on',
                                        offvalue = 'off',
                                        )
        self.legend_switch.pack(side = 'left', pady = 10, padx= 5)

    def _build_right_frame(self):
        # Right frame
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.grid(column = 1,row = 1, sticky ='nsew',padx =5, pady = 10)

        # Setting up initial plot and canvas
        self.fig, self.ax = plt.subplots(figsize=(12,9), dpi=150)
        self.fig.subplots_adjust(
            left=0.05, right=0.95,
            bottom=0.05, top=0.95
        )
        self.canvas = FigureCanvasTkAgg(self.fig, master= self.right_frame)
        self.canvas.get_tk_widget().pack(expand = True, fill = ctk.BOTH) 
        self.setup_plot()
        self.canvas.draw()

    def create_widgets(self):
        self._build_left_frame()
        self._build_top_frame()
        self._build_right_frame()

        
    def setup_plot(self):
        self.ax.set_facecolor('#000000')
        self.ax.autoscale(enable=True, axis='both', tight=False)
        self.ax.tick_params(axis='x', which='major', labelsize = 12, labelrotation = 30)

        self.ax.tick_params(axis='y', which='major', labelsize = 12)

        # Set ticks 
        self.ax.xaxis.set_major_locator(MaxNLocator(nbins=15, integer=True))
        self.ax.yaxis.set_major_locator(MaxNLocator(nbins=15, integer=True))

        # Move x-axis and y-axis to center (origin)
        self.ax.spines['left'].set_position('zero')   # y-axis through x=0
        self.ax.spines['bottom'].set_position('zero') # x-axis through y=0

        # Hide top and right spines
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')

        if self.grid_state.get() == 'on':
            self.ax.grid(True)
        else:
            self.ax.grid(False)


    def plot(self):
        self.ax.clear()
        #self.setup_plot()

        for func in self.functions:
            if func.selected:
                line = func.plot_me(resolution = int(self.resolution_slider.get()))
                self.ax.add_line(line)

        if self.legend_state.get() == 'on':
            self.ax.legend()

        self.canvas.draw()
            

    def save_callback(self):
        extention = self.save_options.get().lower()
        file_path = filedialog.asksaveasfilename(defaultextension=f".{extention}",
                                                   filetypes=[(f"{extention} files", f"*.{extention}"), ("All files", "*.*")])

        if file_path:
            self.fig.savefig(file_path, dpi=300, bbox_inches="tight")
            messagebox.showinfo('Success', f"Graph saved to {file_path}", icon = 'info')


                
    def reset_all(self):
        # Confirm user choice
        if not messagebox.askokcancel("Clear window", "This window will be cleared", icon = 'question'):
            return
        # if the user confirms, proceed with resetting
        self.remove(all = True)
        self.initialize_variables()

        self.grid_switch.deselect()
        self.plot_theme_options.set('classic')
        self.legend_switch.deselect()

        self.resolution_slider.set(100)
        self.slider_label.configure(text = f'Resolution: {100}') 

        self.ax.clear()
        self.setup_plot()
        self.canvas.draw()

        messagebox.showinfo('Info', "Window cleared!", icon = 'info')
    
    
    def bind_events(self):
        # Bind Enter key to the entire window
        self.bind("<Return>", lambda event: self.plot_button.invoke()) 
        # Bind `Control + c`  keys to the entire window
        self.bind("<Control-s>", lambda event: self.save_button.invoke())
        # Bind `Control + r`  keys to the entire window
        self.bind("<Control-r>", lambda event: self.reset_button.invoke())
        #
        self.bind("<Control-a>", lambda event: self.select_all_button.invoke())
            

    def switch_theme(self):
        if self.current_theme.get() == 'light':
            self.current_theme.set('dark')
        else:
            self.current_theme.set('light')
        ctk.set_appearance_mode(self.current_theme.get())



    def slide(self,value):
        self.slider_label.configure(text = f'Resolution: {int(value)}')

    def toggle_left_frame(self):
        if self.left_frame_visible:
            # Hide left frame
            self.left_frame.grid_forget()
            self.toggle_button.configure(image= get_icon(IconName.RIGHT, 40))
            self.grid_columnconfigure(0, weight = 0)
            self.grid_columnconfigure(1, weight = 2)
            self.left_frame_visible = False
        else:
            # Show left frame
            self.left_frame.grid(column=0,row =1, sticky='nsew')
            self.toggle_button.configure(image= get_icon(IconName.LEFT, 40))
            self.grid_columnconfigure(0, weight = 1)
            self.grid_columnconfigure(1, weight = 2)
            self.left_frame_visible = True        

    def add_function(self, function):
        self.functions.append(function)
        function.label.pack(padx= 5, pady =5, fill= "both", expand = True)

    def remove(self, all = False):
        if not all:
            to_remove =[]
            for func in self.functions:
                
                if func.selected:
                    to_remove.append(func)
                    func.label.destroy()
            self.functions= [func for func in self.functions if func not in to_remove]   
            messagebox.showinfo("Success", f"Selected functions removed", icon = 'info')

        else:
            for func in self.functions:
                func.label.destroy()
            func = []
        self.plot()     

    def select_all(self):
        for func in self.functions:
            if not func.selected:
                func.click_label()



    def open_function_window(self):
        if self.function_window is None or not self.function_window.winfo_exists():
            self.function_window = FunctionWindow(parent = self, callback= self.add_function)  # create window if its None or destroyed
            self.function_window.lift()  # Bring to front
            self.function_window.focus_force()  # Force focus
            self.function_window.grab_set()  # Make it modal (optional)
        else:
            self.function_window.lift()  # Bring to front
            self.function_window.focus_force()  # Force focus

