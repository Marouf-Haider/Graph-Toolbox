from sympy import symbols, sympify, lambdify
from numpy import linspace
from customtkinter import CTkLabel
from matplotlib.lines import Line2D

class Function:
    def __init__(self, parent,  name :str, expr:str, settings):
        self.parent = parent
        self.name = name
        self.x = symbols('x')
        self.expr_str = expr
        self.expr_sp = sympify(self.expr_str)
        self.expr_np = lambdify(self.x, self.expr_sp,  modules ='numpy')
        self.settings = settings
        self.selected = False
        self.label = CTkLabel(parent.functions_frame,
                                  text = self.__str__(),
                                  font= ("Roboto",18, "bold", "roman"),
                                  corner_radius=20,
                                  anchor='w'
                                  )
        # Bind click event to the new label (fix closure issue)
        self.label.bind("<Button-1>", lambda event: self.click_label())


    def __str__(self):
        return f'{self.name}(x) = {self.expr_str}'
    
    def __call__(self, value): 
        return self.expr_np(value)

    def evaluate(self, 
                 start : float,
                 end: float,
                resolution: int =  100):
        
        x_values = linspace(start, end, num = resolution)
        return x_values,self.expr_np(x_values)

    def click_label(self):
        if self.selected :
            # Label is selected, deselect it
            self.label.configure(fg_color='transparent')
            self.selected = False
        else:
            # Label is not selected, select it
            self.label.configure(fg_color="#C6988A")
            self.selected = True

    def plot_me(self, resolution):
        x_vals, y_vals = self.evaluate(self.settings['start'],self.settings['end'], resolution)
        line = Line2D(x_vals,
                            y_vals,
                            linestyle   = self.settings['line_option'],
                            linewidth   = self.settings['line_width'],
                            color       = self.settings['line_color'],
                            marker      = self.settings['marker_option'],
                            markersize  = self.settings['marker_size'], 
                            markerfacecolor = self.settings['marker_color'],
                            label = self.__str__()
                                  )
        return line