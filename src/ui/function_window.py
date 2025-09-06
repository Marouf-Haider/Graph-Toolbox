#!.\.venv\Scripts\python.exe

import customtkinter as ctk
from CTkColorPicker import CTkColorPicker
from tkinter import messagebox
from src.function import Function

class FunctionWindow(ctk.CTkToplevel):
    def __init__(self,parent = None, callback= None , *args, **kwargs):
        super().__init__(master = parent, *args, **kwargs)

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        width = 700
        height = 300

        x = int((screen_width - width) / 2)
        y = int((screen_height - height) / 2)

        self.geometry(f"{width}x{height}+{x}+{y}")
        self.resizable(False, False)

        self.parent = parent
        self.callback = callback
        self.title('Add function')
        self.current_color_entry = None  # Track which color entry is being edited
        

        self.line_styles = {
            'None': '',
            'Solid': '-',
            'Dashed': '--',
            'Dash-dot': '-.',
            'Dotted': ':'
            }
        self.marker_styles = {
            'None': '',
            'Circle': 'o',
            'Square': 's',
            'Star': '*',
            'Triangle Up': '^',
            'Cross': 'x'
            }

        # main frame
        self.frame_1 = ctk.CTkFrame(self, corner_radius=0)
        self.frame_1.pack(pady = 0, padx =0, fill = ctk.BOTH, expand = True)


        # color picker 
        self.color_picker = CTkColorPicker(self.frame_1,
                                            command = self.pick_color,
                                            )

        self.color_picker.pack(side = 'right',padx =5, pady =5, expand = True)

        # function frame
        self.frame_2 = ctk.CTkFrame(self.frame_1)
        self.frame_2.pack(pady = 5,padx =10, fill = ctk.BOTH, expand = True)

        self.frame_2.grid_columnconfigure(0, weight= 0)
        self.frame_2.grid_columnconfigure(1, weight= 0)
        self.frame_2.grid_columnconfigure(2, weight= 3)
        self.frame_2.grid_rowconfigure(0, weight=1)

        self.function_label = ctk.CTkLabel(self.frame_2, text='Function', font=("Roboto", 16, 'bold'))
        self.function_label.grid(column = 0, row =0,padx = 10, pady=5, sticky ='nsew')

        # name entry
        self.name = ctk.CTkEntry(master= self.frame_2, 
                                           placeholder_text=f"Name",
                                           width =60,
                                             font=("Roboto", 16))
        self.name.grid(column  = 1, row =0,padx = 5,pady=5, sticky ='nsew' )
        self.name.insert(0,'f')
        # Function entry
        self.function = ctk.CTkEntry(master= self.frame_2, 
                                           placeholder_text='Expression',
                                             font=("Roboto", 16))
        self.function.grid(column  = 2, row =0,padx = 5,pady=5, sticky ='nsew' )

        # start/end frame
        self.frame_3 = ctk.CTkFrame(self.frame_1)
        self.frame_3.pack(pady = 5, padx =10, fill = ctk.BOTH, expand = True)
        self.frame_3.grid_columnconfigure((0,2), weight= 0)
        self.frame_3.grid_columnconfigure((1,3), weight= 1)
        self.frame_3.grid_rowconfigure(0, weight= 1)


        self.start_label = ctk.CTkLabel(self.frame_3, text='Start', font=("Roboto", 16, 'bold'))
        self.start_label.grid(column= 0,row=0,pady=10,padx= 5, sticky ='nsew')

        # Start point entry
        self.start = ctk.CTkEntry(self.frame_3, 
                                        placeholder_text="Start point",
                                        font=("Roboto", 16))
        self.start.grid(column= 1,row=0,pady=10,padx= 5, sticky ='nsew')
        self.start.insert(0,'-100')
        self.end_label = ctk.CTkLabel(self.frame_3,
                                       text='End', 
                                       font=("Roboto", 16, 'bold'))
        self.end_label.grid(column= 2,row=0,pady=10,padx= 5, sticky ='nsew')

        # End point entry
        self.end = ctk.CTkEntry(self.frame_3,
                                       placeholder_text="End point",
                                         font=("Roboto", 16))
        self.end.grid(column= 3,row=0,pady=10,padx= 5, sticky ='nsew')   
        self.end.insert(0,'100')
        # plot line frame
        self.frame_5 = ctk.CTkFrame(self.frame_1)
        self.frame_5.pack(pady = 5, padx =10, fill = ctk.BOTH, expand = True)
        self.frame_5.grid_columnconfigure(0, weight= 0)
        self.frame_5.grid_columnconfigure((1,2), weight= 1)
        self.frame_5.grid_rowconfigure(0, weight= 1)


        self.line_label = ctk.CTkLabel(self.frame_5, text='Line', font=("Roboto", 16, 'bold'))
        self.line_label.grid(column= 0,row=0,pady=10,padx= 10, sticky ='nsew') 
        # plot line type
        self.line_option = ctk.CTkOptionMenu(self.frame_5,
                                        values = list(self.line_styles.keys()), 
                                        font=("Roboto", 16, 'bold')
                                            )
        self.line_option.grid(column= 1,row=0,pady=10,padx= 5, sticky ='nse') 
        self.line_option.set("Solid")

        # line color entry
        self.line_color =  ctk.CTkEntry(self.frame_5, 
                                        placeholder_text= 'Color',
                                        font=("Roboto", 16)
                
                                        )
        self.line_color.grid(column= 2,row=0,pady=10,padx= 5, sticky ='nse') 
        self.line_color.insert(0,"#5495ff")

        # plot marker frame
        self.frame_6 = ctk.CTkFrame(self.frame_1)
        self.frame_6.pack(pady = 5, padx =10, fill = ctk.BOTH, expand = True)
        self.frame_6.grid_columnconfigure(0, weight= 0)
        self.frame_6.grid_columnconfigure((1,2), weight= 1)
        self.frame_6.grid_rowconfigure(0, weight= 1)

        self.marker_label = ctk.CTkLabel(self.frame_6, text='Marker',font=("Roboto", 16, 'bold'))
        self.marker_label.grid(column= 0,row=0,pady=10,padx= 10, sticky ='nsew') 
        # markers type
        self.marker_option = ctk.CTkOptionMenu(self.frame_6,
                                        values = list(self.marker_styles.keys()),
                                        font=("Roboto", 16, 'bold')
                                            )
        self.marker_option.grid(column= 1,row=0,pady=10,padx= 5, sticky ='nse') 
        self.marker_option.set("Circle")
        # marker color
        self.marker_color =  ctk.CTkEntry(self.frame_6, placeholder_text= 'Color',font=("Roboto", 16))
        self.marker_color.grid(column= 2,row=0,pady=10,padx= 5, sticky ='nse') 
        self.marker_color.insert(0,"#5495ff")


        # Add button
        self.add_button = ctk.CTkButton(self, text= 'Add', command =self.export_data)
        self.add_button.pack(side='right', pady =  10, padx =20)
        # Cancel button
        self.cancel_button = ctk.CTkButton(self, text= 'Cancel', command=self.destroy)
        self.cancel_button.pack(side= 'right' ,pady =  10, padx =20)


        self.line_color.bind('<Button-1>', lambda event: self.acquire(self.line_color))
        self.marker_color.bind('<Button-1>', lambda event: self.acquire(self.marker_color))

        self.bind('<Return>', lambda event: self.add_button.invoke())

    
    def acquire(self, entry):
        self.current_color_entry = entry
        self.current_color_entry.focus_set()


    def pick_color(self,color):
        if self.current_color_entry:
            self.current_color_entry.delete(0, 'end')
            self.current_color_entry.insert(0, color)

    def export_data(self):
        # Validate inputs
        if not self.validate_inputs():
            return
        # Prepare function data

        settings = {
            'start': float(self.start.get()),
            'end': float(self.end.get()),
            'line_option': self.line_styles[self.line_option.get()],
            'line_color': self.line_color.get(),
            'line_width': 2,
            'marker_option': self.marker_styles[self.marker_option.get()],
            'marker_color': self.marker_color.get(),
            'marker_size': 2,
        }
        func = Function(parent = self.parent , name = self.name.get(), expr = self.function.get(), settings= settings)

        # Send data to parent
        self.parent.add_function(func)
        self.destroy()


    def validate_inputs(self):
        if not self.name.get().strip():
            messagebox.showerror("Error", "Please enter the function's name", icon = 'error')
            return False
        if len(self.name.get().strip()) > 1:
            messagebox.showerror("Error", "Function's name must be a single letter", icon = 'error')
            return False
        # Check if function is entered
        if not self.function.get().strip():
            messagebox.showerror("Error", "Please enter a function", icon = 'error')
            return False
        
        # Check start and end values
        try:
            start = float(self.start.get())
            end = float(self.end.get())
            if start >= end:
                messagebox.showerror("Error", "Start value must be less than end value", icon = 'error')
                return False
        except ValueError:
            messagebox.showerror("Error", "Please enter valid start and end values", icon = 'error')
            return False
        
        return True

if __name__== "__main__":
    test_app = FunctionWindow()
    test_app.mainloop()