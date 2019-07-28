from tkinter import *
from tkinter.font import Font
import subprocess, string
from components import requests, result, settings
from components.constants import *


keyboard = list(string.ascii_lowercase) + [str(i) for i in range(0, 10)] + ['space', '-', '_', 'BackSpace']

class Launcher(Tk):
    def __init__(self, *args, **kwargs):
        Tk.__init__(self, *args, **kwargs) 
    # Defining the main_window aspects
        self.iconbitmap('./components/icons/rocket-icon.ico')
        self.title("Rocket Launcher")
        self.format = formats
    # Defining the widgets
        self.container = Frame(
            master=self,
            bg='white'
        )
        self.container.pack(
            fill='x',
            expand=False
        )

        self.format_icon = Label(
            master=self.container, 
            bg='white'
        )
        self.icon_image = PhotoImage(file='./components/icons/refresh.png')
        self.format_icon.grid(
            row=0, 
            column=0, 
            ipadx=8, 
            ipady=8, 
            padx=5, 
            sticky=E
        )

        self.entry = Entry(
            master=self.container, 
            font=Font(family="Helvetica",size=10, weight='normal'), 
            bg='white', 
            relief='flat'
        )
        self.entry.grid(
            row=0, 
            column=1,
            ipady=8,
            ipadx=50,
            sticky=W
        )
        self.entry_placeholder = "type  name"
        self.entry.insert(0, self.entry_placeholder)

        self.button = Button(
            master=self.container, 
            bg='white', 
            relief='flat'
        )
        self.button_image = PhotoImage(file='./components/icons/setting.png')
        self.button.config(
            image=self.button_image, 
            height='15', 
            width='15')
        self.button.grid(
            row=0, 
            column=2, 
            ipadx=8, 
            ipady=8,
            padx=5,
            sticky=E
        )
        
        self.results_list = []
        self.results_frame = Frame(
            master=self, 
            relief='raised',
            bg='yellow'
        )
        self.results_frame.pack(
            side=BOTTOM, 
            anchor=NW,
            expand=False,
            ipadx=0
        )
        self.results_frame.pack_propagate(0)
    # Binding events
        self.entry.bind('<Button-1>', self.remove_placeholder)
        self.entry.bind('<Return>', self.entry_treatment, add='+')
        self.entry.bind('<Double-space>', self.set_icon, add='+')
        self.entry.event_add(
            '<<KeyboardRelease>>',
            *['<KeyRelease-{}>'.format(key) for key in keyboard]
        )
        self.entry.bind('<<KeyboardRelease>>', self.give_suggestions, add='+')
        self.button.bind('<Button-1>', self.open_settings)


    def remove_placeholder(self, event):
        if self.entry.get() == self.entry_placeholder:
            self.entry.delete(0, len(self.entry_placeholder))
        return

    def clear_suggestions(self):
        for child in self.results_frame.winfo_children():
            child.grid_forget()

    def give_suggestions(self, event):
        self.clear_suggestions()
        entry = self.entry.get()

        if '  ' in entry:
            format, pattern = entry.split(sep='  ')
            suggestions_dict = requests.suggestions(format, pattern)
            if pattern != '':
                for name in suggestions_dict.keys():
                    path = suggestions_dict[name]

                    new_result = result.Result(
                        master=self.results_frame, 
                        name=name, 
                        path=path, 
                        format=format,
                        bg='white'
                    )
                    new_result.grid(
                        sticky=W
                    )

                    def choose_result(event, format=format, path=path):
                        print(format, '  ', path)
                        self.entry.delete(0, len(self.entry.get()))
                        self.entry.insert(0, format + '  ' + path)
                    for child in new_result.winfo_children():
                        child.bind('<Button-1>', choose_result)

    def entry_treatment(self, event):
        request = self.entry.get()
        if '  ' in request:
            command, research = request.split(sep = '  ')

            if command == 'google':
                research = research.replace(' ', '+')
                subprocess.run('start www.google.com/search?q={}'.format(research), shell=True)

            elif command == 'youtube':
                research = research.replace(' ', '+')
                subprocess.run('start www.youtube.com/search?q={}'.format(research), shell=True)

            elif command == 'wiki':
                research = research.replace(' ', '_')
                subprocess.run('start https://en.wikipedia.org/wiki/{}'.format(research), shell=True)

            elif command == 'amazon':
                research = research.replace(' ', '+')
                subprocess.run('start www.amazon.fr/s?k={}'.format(research), shell=True)

            elif command == 'open':
                subprocess.call("start {}".format(research), shell=True) # enter a directory

            elif command == 'anki':
                subprocess.run("C:/Program Files/Anki/anki.exe", shell=True)

            elif command == 'drive':
                subprocess.run("start https://drive.google.com/drive/my-drive", shell=True)
            
            elif command == 'cmd':
                subprocess.run("start cmd", shell=True)
            
            elif command == 'shell':
                subprocess.run("start powershell", shell=True)

            elif command in self.format:
                subprocess.run("start {}".format(research), shell=True)
            
            self.entry.delete(0, len(request))
        return

    def open_settings(self, event):
        setting_window = settings.Settings(self)
        return

    def set_icon(self, event):
        format = self.entry.get()[:-1]

        if format in self.format:
            try :
                self.icon_image = PhotoImage(file='./components/icons/{}.png'.format(format))
            except :
                self.icon_image = PhotoImage(file='./components/icons/file.png')
        
        self.format_icon.config(
            image=self.icon_image,
            height='15',
            width='15'
        )

