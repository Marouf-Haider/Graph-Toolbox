import customtkinter as ctk


class ButtonsGrid(ctk.CTkFrame):
    def __init__(self, m: int, n:int, buttons_color=None, master= None, width = 150, height = 150, corner_radius = None, border_width = None, bg_color = "transparent", fg_color = None, border_color = None, background_corner_colors = None, overwrite_preferred_drawing_method = None, **kwargs):
        super().__init__(master, width, height, corner_radius, border_width, bg_color, fg_color, border_color, background_corner_colors, overwrite_preferred_drawing_method, **kwargs)

        self.width  = 20*m 
        self.height = 15*n

        super().__init__(master,self.width, self.height,**kwargs)

        self.m = m
        self.n = n
        self.buttons_color = buttons_color
        self.buttons_dict = {}
        self.grid_columnconfigure(tuple(range(self.m)),weight=1)
        self.grid_rowconfigure(tuple(range(self.n)) , weight=1)

        self._create_buttons()

    def _create_buttons(self):
        for i in range(self.m):
            for j in range(self.n):
                button = ctk.CTkButton(self, text='empty', font= ('Roboto', 18,'bold'), width=40, fg_color=self.buttons_color)
                button.grid(column = i, row = j, sticky= 'nsew', padx = 10,pady=10)
                self.buttons_dict[f'({i},{j})'] = button

    def set_callback(self,i,j, callback):
        self.buttons_dict[f'({i},{j})'].configure(command = callback)

    def from_dict(master, data: dict , shape:tuple[int,int], buttons_color = None):
        m, n = shape
        if m*n < len(data):
            raise ValueError('There are more labels than buttons!')
        else:
            buttons = ButtonsGrid(m,n,master = master, buttons_color=buttons_color)
            labels = list(data.keys())
            for i,text in enumerate(labels):
                buttons.buttons_dict[f'({i%m},{i//m})'].configure(text = text,
                                                                  command= data[text] or None)
            return buttons
