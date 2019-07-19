import tkinter as tk

root = tk.Tk()

frame = tk.Frame(
    master=root,
    bg='yellow'
)
frame.pack(
    expand=True,
    fill='both',
    ipadx=0
)

label = tk.Label(
    master=frame,
    text='Hello World!',
    bg='red',
    fg='white'
)
label.pack(
    expand=True,
    fill='x'
)


root.mainloop()