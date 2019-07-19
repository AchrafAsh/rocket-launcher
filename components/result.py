from tkinter import *
from tkinter.font import Font
from components.constants import *


class Result(Frame):
    def __init__(self, master, name, path, format, *args, **kwargs):
        Frame.__init__(self, master, *args, **kwargs)
    # Attributes
        self.name = name
        self.path = path
        self.format = format
        self.icon_image = 0
        self.get_image()
    # Widgets
        self.icon = Label(
            master=self, 
            bg='white'
        )
        self.icon.grid(
            row=0,
            column=0,
            rowspan=2,
            padx=5,
            sticky=W
        )
        self.icon.config(
            image=self.icon_image
        )

        self.name_label = Label(
            master=self, 
            text=self.name, 
            font=Font(family='Helvetica', size=11, weight='bold'),
            bg='white'
        )
        self.name_label.grid(
            row=0, 
            column=1,
            sticky=W
        )

        self.path_label = Label(
            master=self, 
            text=self.path,
            font=Font(family='Helvetica', size=6, slant='italic'),
            bg='white'
        )
        self.path_label.grid(
            row=1, 
            column=1,
            sticky=W
        )
    # Binding
        for child in self.winfo_children():
            child.bind('<ButtonPress-1>', self.turn_blue)
            child.bind('<ButtonRelease-1>', self.back_to_white)

    def get_image(self):
        if self.format in formats:
            try :
                self.icon_image = PhotoImage(file=absolute_path+'/components/icons/{}.png'.format(self.format))
            except :
                self.icon_image = PhotoImage(file=absolute_path+'/components/icons/file.png')
        else:
            return None

    def turn_blue(self, event):
        self.config(bg='orange')
        for child in self.winfo_children():
            child.config(bg='orange')
    
    def back_to_white(self, event):
        self.config(bg='white')
        for child in self.winfo_children():
            child.config(bg='white')

