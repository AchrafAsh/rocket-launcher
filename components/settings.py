from tkinter import *
from tkinter.font import Font
import traceback
from components import requests
from components.constants import *


class Settings(Toplevel):
    def __init__(self, master, *args, **kwargs):
        Toplevel.__init__(self, master, *args, **kwargs)
    # Window features
        self.title("Settings")
        self.iconbitmap(absolute_path+'/components/icons/settings.ico')
    # Widgets
        self.container = Frame(master=self)
        self.container.pack(
            fill=BOTH, 
            expand=True
        )
        
        self.indication = Label(
            master=self.container, 
            text='Enter a path to browse and check the format to load'
        )
        self.indication.grid(
            row=0, 
            column=0
        )

        self.new_path_entry = Entry(master=self.container)
        self.new_path_entry.grid(
            row=1, 
            ipadx=50
        )

        self.format_preferences = Frame(
            master=self.container
        )
        self.format_preferences.grid(
            row=2, 
            column=0,
            padx=20,
            pady=5
        )

        self.format = []
        for format in programming + images + videos + files :
            var = IntVar()
            checkbutton = Checkbutton(
                master=self.format_preferences, 
                text=format, 
                variable=var
            )
            self.format.append([
                    format,
                    var,
                    checkbutton
            ])
            checkbutton.grid(
                row=(len(self.format)-1)%6, 
                column=(len(self.format)-1)//6, 
                sticky=W
            )
        var = IntVar()
        self.all_checkbutton = Checkbutton(
            master=self.format_preferences, 
            text='all',
            variable=var
        )
        def check_everything(event, var=var):
            for checkbutton in self.format :
                checkbutton[1].set(1-var.get())

        self.all_checkbutton.grid(
            row=6, 
            sticky=W
        )
        self.all_checkbutton.bind('<Button-1>', check_everything)

        self.submit_new_path = Button(
            master=self.container, 
            text='add',
            bg='red',
            fg='white'
        )
        self.submit_new_path.grid(
            row=3, 
            sticky=E,
            padx=2
        )
        
        self.reboot = Button(
            master=self.container, 
            text='reboot',
            bg='red',
            fg='white'
        )
        self.reboot.grid(
            row=4, 
            sticky=E,
            padx=2
        )
        
        self.answer = Label(
            master=self,
            bg='grey'
        )
        self.answer.pack(side='bottom')
        # Binding events
        self.reboot.bind('<Button-1>', self.reboot_database)
        self.submit_new_path.bind('<Button-1>', self.load)

    def load(self, event):
        preferences = []
        for i in range(len(self.format)):
            if self.format[i][1].get() == 1:
                preferences.append(self.format[i][0])
        try:
            requests.load_database(self.new_path_entry.get(), preferences)
        except Exception:
            print(traceback.print_exc())
            self.answer.config(text=traceback.print_exc())
        else:
            print('Succefully loaded')
            self.answer.config(text='Succefully loaded')
            self.new_path_entry.delete(0, len(self.new_path_entry.get()))
        return

    def reboot_database(self, event):
        alert = Toplevel(self)
        alert_message = Label(alert, text='Are you sure you want to reboot the database ?')
        alert_message.grid(row=0, columnspan=2)
        
        def reboot():
            requests.clear_database()
            alert.withdraw()

        yes_button = Button(alert, text='Yes', command=reboot)
        yes_button.grid(row=1, column=0, sticky=E)
        no_button = Button(alert, text='No', command=alert.withdraw)
        no_button.grid(row=1, column=1, sticky=W)