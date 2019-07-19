import requests
import sqlite3
import subprocess
from tkinter import *

root = Tk()

entry = Entry(
    master=root
)
entry.grid(
    row=0,
    column=0
)

listbox = Frame(
    master=root
)
listbox.grid(
    row=1,
    column=0
)
image = PhotoImage(
        file='./icons/folder.png'
)

label = Label(
    master=listbox,
    text='click me please',
    fg='black',
    bg='white'
)
label.grid(
    row=0, 
    column=0,
    ipadx=50,
    ipady=50
)
def get_blue(event):
    label.config(bg='orange')

def back_to_normal(event):
    label.config(bg='white')

label.bind('<ButtonPress-1>', get_blue)
label.bind('<ButtonRelease-1>', back_to_normal)

root.mainloop()