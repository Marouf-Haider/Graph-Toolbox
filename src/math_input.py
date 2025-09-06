#!.\.venv\Scripts\python.exe

import customtkinter as ctk
import sympy as sp

from io import BytesIO
import matplotlib.pyplot as plt
from PIL import Image

from ui.buttons_grid import ButtonsGrid

class MathInput(ctk.CTkFrame):
    def __init__(self, master, width = 200, height = 200, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.to_display = ['.']
        self.cursor_index = 0

        self.display_screen = ctk.CTkLabel(self,
                                            height =120,
                                           text = '',
                                            fg_color="#FFFFFF",
                                            corner_radius=15
                                            )
        self.display_screen.pack(side= 'top',anchor ='n',fill ="x", expand=False, padx=10,pady=10, ipadx =0, ipady =0)
        self.screen = ctk.CTkEntry(self,
                                    height =50,
                                    font= ('Roboto', 25, 'bold'),
                                    border_width=0.5
                                    )
        self.screen.pack(side= 'top',anchor ='n', expand=False, fill='x', padx=10,pady=10)
        self.screen.configure(state= 'disabled')
        #self.after(100, self.screen.focus)

        self.edits = self.Edit_buttons(self)
        self.edits.pack(side= 'top',anchor ='n', expand=False, fill='both', padx=10,pady=10)
        self.num_pad = self.NumPad(self)
        self.num_pad.pack(side= 'right',anchor ='e', expand=True, fill='both', padx=10,pady=10)
        self.vars = self.variables_buttons(self)
        self.vars.pack(side= 'left',anchor ='w', expand=True, fill='both', padx=10,pady=10)
        self.operations = self.operations_buttons(self)
        self.operations.pack(side= 'left',anchor ='center', expand=True, fill='both', padx=10,pady=10)
        self.trigonometric =self.Trigonometric_Functions(self)
        self.trigonometric.pack(side= 'left',anchor ='center', expand=True, fill='both', padx=10,pady=10)

        constants = {
                     'π': lambda: self._write_on_screen(['\\pi']),
                     'φ': lambda: self._write_on_screen(['\\phi']),
                     'e': lambda: self._write_on_screen(['\\mathit{e}']),
                     'i': lambda: self._write_on_screen(['\\mathit{i}']),

        }
        other_functions = {
                    'log': lambda: self._write_on_screen(['\\log']),
                    'exp': lambda: self._write_on_screen(['\\exp']),
                    'abs': lambda: self._write_on_screen(['\\|','\\|'])
        }

    def variables_buttons(self, master):
        dict = {
            'x': lambda: self._write_on_screen(['x']),
            'y': lambda: self._write_on_screen(['y']),
            'z': lambda: self._write_on_screen(['z']),
        }
        buttons = ButtonsGrid.from_dict(master,dict,(1,3), buttons_color="#788AFF")
        return buttons

    def operations_buttons(self, master):
        dict = {
                     '(': lambda: self._write_on_screen(['(']),
                     ')': lambda: self._write_on_screen([')']),
                     '+': lambda: self._write_on_screen(['+']),
                     '-': lambda: self._write_on_screen(['-']),
                     '⨯': lambda: self._write_on_screen(['*']),
                     '/': lambda: self._write_on_screen(['\\frac{','}{','}']),
                     '√': lambda: self._write_on_screen(['\\sqrt{','}']),
                     '^': lambda: self._write_on_screen('^'),
                       }
        buttons = ButtonsGrid.from_dict(master,dict,(3,3))
        return buttons
    
    def move_cursor_left(self):
        if self.cursor_index > 0:
            self.to_display.pop(self.cursor_index)
            self.cursor_index -= 1
            self.to_display = self.to_display[:self.cursor_index] +['.'] + self.to_display[self.cursor_index:]
            self._update_screens()
    
    def move_cursor_right(self):
        if self.cursor_index < len(self.to_display)-1:
            self.to_display.pop(self.cursor_index)
            self.cursor_index += 1
            self.to_display = self.to_display[:self.cursor_index] +['.'] + self.to_display[self.cursor_index:]
            self._update_screens()   

    def Edit_buttons(self, master):
        dict = {
                    '-->': lambda: self.move_cursor_right() ,
                    '<--': lambda: self.move_cursor_left(),
                     'CLA': lambda:self._clear_all(),
                     'CL': lambda: self._clear_last(),
                     'Space': lambda: self._write_on_screen(['\\quad '])
        }
        buttons = ButtonsGrid.from_dict(master,dict,(6,1), buttons_color="#8A92EA")
        buttons.buttons_dict['(5,0)'].destroy()
        buttons.buttons_dict['(4,0)'].grid(columnspan =4)
        return buttons
    
    def Trigonometric_Functions(self, master):
        dict = {
                    'sin': lambda: self._write_on_screen(['\\sin ']),
                    'cos': lambda: self._write_on_screen(['\\cos ']),
                    'tan': lambda: self._write_on_screen(['\\tan ']),
                    'arccos': lambda: self._write_on_screen(['\\arccos ']),
                    'arcsin': lambda: self._write_on_screen(['\\arcsin ']),
                    'arctan': lambda: self._write_on_screen(['\\arctan ']),
                    'sinh': lambda: self._write_on_screen(['\\sinh ']),
                    'cosh': lambda: self._write_on_screen(['\\cosh ']),
                    'tanh': lambda: self._write_on_screen(['\\tanh '])
        }
        buttons = ButtonsGrid.from_dict(master,dict,(3,3), buttons_color="#B9AE14")
        return buttons

    def NumPad(self, master):
        dict = {f'{i}': lambda i = i: self._write_on_screen(f'{i}') for i in range(10)}
        num_pad = ButtonsGrid.from_dict(master ,dict,(4,3), buttons_color="#14B97C")
        num_pad.buttons_dict['(2,2)'].destroy()
        num_pad.buttons_dict['(3,2)'].destroy()
        return num_pad


    def render_expression(self):
        expr = self.to_display[:self.cursor_index]+ self.to_display[self.cursor_index+1:]
        expr = ''.join(expr)
        buf = BytesIO()
        fig, ax = plt.subplots()
        ax.text(0.5, 0.5, f'${expr}$', fontsize = 50, ha='center', va='center')
        ax.axis('off')
        plt.savefig(buf, format='png', bbox_inches='tight', transparent=True, dpi = 100)
        plt.close(fig)
        buf.seek(0)
        return Image.open(buf)

    def _update_screens(self):
        text =''.join(self.to_display)

        self.screen.configure(state = 'normal')
        self.screen.delete(0,'end')
        self.screen.insert(0,text)
        self.screen.configure(state = 'disabled')

        if self.to_display != []:
            temp_img = self.render_expression()
            img = ctk.CTkImage(light_image = temp_img ,dark_image=temp_img, size= (500,115)) 
            self.display_screen.configure(image=img)

    def _write_on_screen(self, text: list[str]):
        for txt in text:
            self.to_display.append(txt)
            self._update_screens()
    
    def _clear_last(self):
        if self.to_display:
            self.to_display.pop()
            self._update_screens()

    def _clear_all(self):
        self.to_display = []
        self.display_screen.configure(image=None)
        self._update_screens()


class test_app(ctk.CTk):
    def __init__(self):
        super().__init__()
        # Configure window
        self.title("Math input")
        width = int(self.winfo_screenwidth()*0.7)
        height = int(self.winfo_screenheight()*0.7)
        self.geometry(f"{width}x{height}+0+0")
        self.minsize(width,height)
        self.math_keyboard = MathInput(self, corner_radius=0)
        self.math_keyboard.pack(fill = 'both', expand = True )


if __name__ =='__main__':

    ctk.set_appearance_mode("light")  
    ctk.set_default_color_theme("theme\\my_theme.json") 
    app = test_app()
    app.mainloop()